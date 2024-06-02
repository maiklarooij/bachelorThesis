import weaviate

from typing import List, Any, Dict
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.query import MetadataQuery
from weaviate.classes.query import Filter


def get_datatype(type_string):
    if type_string == "text":
        return DataType.TEXT
    if type_string == "textList":
        return DataType.TEXT_ARRAY
    if type_string == "int":
        return DataType.INT
    if type_string == "intList":
        return DataType.INT_ARRAY
    if type_string == "boolean":
        return DataType.BOOL
    if type_string == "booleanList":
        return DataType.BOOL_ARRAY
    if type_string == "number":
        return DataType.NUMBER
    if type_string == "numberList":
        return DataType.NUMBER_ARRAY
    if type_string == "date":
        return DataType.DATE
    if type_string == "dateList":
        return DataType.DATE_ARRAY
    if type_string == "uuid":
        return DataType.UUID
    if type_string == "uuidList":
        return DataType.TEXT
    if type_string == "blob":
        return DataType.BLOB
    if type_string == "object":
        return DataType.OBJECT
    if type_string == "objectList":
        return DataType.OBJECT_ARRAY
    else:
        raise Exception("Incorrect data type")

def get_filters(governments, meeting_types, years, speakers, videos, min_time, max_time):
    filters = None
    # Removes empty string elements.
    governments = list(filter(lambda x: x != "", governments))
    meeting_types = list(filter(lambda x: x != "", meeting_types))
    years = list(filter(lambda x: x != "", years))
    speakers = list(filter(lambda x: x != "", speakers))
    videos = list(filter(lambda x: x != "", videos))

    if filters is None and len(governments) > 0:
        filters = Filter.by_property("government").contains_any(governments)
    elif len(governments) > 0:
        filters = filters & Filter.by_property("government").contains_any(governments)

    if filters is None and len(meeting_types) > 0:
        filters = Filter.by_property("type").contains_any(meeting_types)
    elif len(meeting_types) > 0:
        filters = filters & Filter.by_property("type").contains_any(meeting_types)

    if filters is None and len(years) > 0:
        filters = Filter.by_property("year").contains_any(years)
    elif len(years) > 0:
        filters = filters & Filter.by_property("year").contains_any(years)

    if filters is None and len(speakers) > 0:
        filters = Filter.by_property("speaker").contains_any(speakers)
    elif len(speakers) > 0:
        filters = filters & Filter.by_property("speaker").contains_any(speakers)

    if filters is None and len(videos) > 0:
        filters = Filter.by_property("code").contains_any(videos)
    elif len(videos) > 0:
        filters = filters & Filter.by_property("code").contains_any(videos)

    if filters is None and (min_time != -1 and min_time is not None):
        filters = Filter.by_property("start").greater_than(min_time)
    elif min_time != -1 and min_time is not None:
        filters = filters & Filter.by_property("start").greater_than(min_time)

    if filters is None and (max_time != -1 and max_time is not None):
        filters = Filter.by_property("end").less_than(max_time)
    elif max_time != -1 and max_time is not None:
        filters = filters & Filter.by_property("end").less_than(max_time)

    return filters

class Weaviate:
    def __init__(self, host="localhost", port="8080"):
        self.client = weaviate.connect_to_custom(
            http_host=host,
            http_port=port,
            http_secure=False,
            grpc_host=host,
            grpc_port=50051,
            grpc_secure=False,
        )
        # self.client = weaviate.connect_to_local()

    def destroy(self):
        self.client.close()

    def get_info(self):
        info = {
            "live": self.client.is_live(),
            "connected": self.client.is_connected(),
            "meta": self.client.get_meta(),
        }

        return info

    def get_all_collections(self):
        return self.client.collections.list_all()


    def get_collection_info(self, name: str):
        collection = self.client.collections.get(name)
        return collection.config.get()


    def create_collection(self, config):
        self.client.collections.create(
            config.name,
            properties=[
                Property(name=p.name, data_type=get_datatype(p.data_type))
                for i, p in enumerate(config.properties)
            ],
            vector_index_config=Configure.VectorIndex.hnsw()
            if config.vector_index_hnsw
            else Configure.VectorIndex.flat(),
        )

    def create_transcripts_collection(self, config):
        self.client.collections.create(
            config.name,
            properties=[
                Property(name=p.name, data_type=get_datatype(p.data_type))
                for i, p in enumerate(config.properties)
            ],
            vectorizer_config=[
                Configure.NamedVectors.none(name="text"),
                Configure.NamedVectors.none(name="speaker"),
            ],
        )


    def delete_collection(self, name: str):
        self.client.collections.delete(name)


    # TODO: Error handling.
    def insert_single_object(self, collection_name: str, obj, vector):
        collection = self.client.collections.get(collection_name)
        uuid = collection.data.insert(
            properties=obj,
            vector=vector,
        )

        return uuid


    def insert_objects(self, collection_name: str, objs: List[Dict[str, Any]]):
        collection = self.client.collections.get(collection_name)
        with collection.batch.dynamic() as batch:
            for o in objs:
                batch.add_object(
                    properties=o["object"],
                    vector=o["vector"],
                )


    def delete_object_uuid(self, collection_name: str, uuid):
        collection = self.client.collections.get(collection_name)
        collection.data.delete_by_id(uuid)


    def delete_objects_filter(self, collection_name: str, filter):
        collection = self.client.collections.get(collection_name)
        collection.data.delete_many(where=filter)


    def get_object_by_id(self, collection_name: str, uuid):
        collection = self.client.collections.get(collection_name)
        return collection.query.fetch_object_by_id(
            uuid
        )

    def search_bm25(
        self,
        collection,
        query,
        limit,
        target_vec,
        governments,
        meeting_types,
        years,
        speakers,
        videos,
        min_time,
        max_time,
        query_properties=["text^2"],
    ):
        c = self.client.collections.get(collection)
        response = c.query.bm25(
            query=query,
            limit=limit,
            filters=get_filters(
                governments, meeting_types, years, speakers, videos, min_time, max_time
            ),
            query_properties=query_properties,
            return_metadata=MetadataQuery(score=True),
        )

        # print(response.objects)
        # print(type(response.objects))

        objs = [
            {
                "properties": o.properties,
                "uuid": str(o.uuid),
                "vector": o.vector,
                "score": o.metadata.score,
            }
            for o in response.objects
        ]

        return objs

    def search_vector(
        self,
        collection,
        vector,
        limit,
        target_vec,
        governments,
        meeting_types,
        years,
        speakers,
        videos,
        min_time,
        max_time,
    ):
        c = self.client.collections.get(collection)

        # TODO: Verify collection exists.
        response = c.query.near_vector(
            near_vector=vector,
            limit=limit,
            target_vector=target_vec,
            # distance=4,
            filters=get_filters(
                governments, meeting_types, years, speakers, videos, min_time, max_time
            ),
            return_metadata=MetadataQuery(distance=True),
        )
        # TODO: Verify search was succeful

        # print(response.objects)
        # print(type(response.objects))

        objs = [
            {
                "properties": o.properties,
                "uuid": str(o.uuid),
                "vector": o.vector,
                "score": o.metadata.distance,
            }
            for o in response.objects
        ]

        return objs

    def search_hybrid(
        self,
        collection,
        query,
        vector,
        limit,
        target_vec,
        alpha,
        governments,
        meeting_types,
        years,
        speakers,
        videos,
        min_time,
        max_time,
        query_properties=["text^2"],
    ):
        c = self.client.collections.get(collection)
        response = c.query.hybrid(
            query=query,
            alpha=alpha,
            query_properties=query_properties,  # Play around with these settings.
            limit=limit,
            target_vector=target_vec,
            vector=vector,
            filters=get_filters(
                governments, meeting_types, years, speakers, videos, min_time, max_time
            ),
            return_metadata=MetadataQuery(score=True, explain_score=True),
        )

        # print(response.objects)
        # print(type(response.objects))

        objs = [
            {
                "properties": o.properties,
                "uuid": str(o.uuid),
                "vector": o.vector,
                "score": o.metadata.score,
            }
            for o in response.objects
        ]

        return objs

    def get_context(self, collection, government, meeting_type, year, video, speech_num):
        c = self.client.collections.get(collection)

        filters = (
            Filter.by_property("government").equal(government)
            & Filter.by_property("type").equal(meeting_type)
            & Filter.by_property("year").equal(year)
            & Filter.by_property("code").equal(video)
            & Filter.by_property("speechNumber").equal(speech_num)
        )

        response = c.query.fetch_objects(
            return_properties=["text"],
            filters=filters,
        )

        objs = [
            {
                "properties": o.properties,
                "uuid": str(o.uuid),
            }
            for o in response.objects
        ]

        return objs

    def get_speaker_name(self, transcript_collection, speaker_collection, video, speakerID):
        tc = self.client.collections.get(transcript_collection)
        filters = (
            Filter.by_property("code").equal(video)
            & Filter.by_property("speaker").equal(speakerID)
        )
        response = tc.query.fetch_objects(
            filters=filters,
            limit=1,
            include_vector=True,
        )
        if len(response.objects) == 0:
            print(speakerID, "not found in transcripts weaviate.")
            return "inspreker"

        speech_vector = response.objects[0].vector["speaker"]
        sc = self.client.collections.get(speaker_collection)
        speaker_response = sc.query.near_vector(
            near_vector=speech_vector,
            return_properties=["name"],
            distance=0.5,
            limit=1,
            return_metadata=MetadataQuery(distance=True),
        )

        # print("speaker response", speaker_response)
        if len(speaker_response.objects) == 0:
            return  "inspreker"

        name = speaker_response.objects[0].properties["name"]
        return  name
