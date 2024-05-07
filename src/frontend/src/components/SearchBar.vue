<script setup>
import { ref, watch } from 'vue';

const searchQuery = ref("")
const searchResults = ref([])

const emit = defineEmits(["newResults", "newQuery"])

const props = defineProps({
    limit: Number,
    alpha: Number,
    method: String,
    gemeente: String,
    type: String,
    year: String,
    speaker: String,
    video: String,
})

watch(searchResults, (searchResults, _) => {
    emit("newResults", searchResults)
})

async function vectorBM25() {
    const gemeentes = []
    if (props.gemeente.length > 0) {
        gemeentes.push(props.gemeente)
    }
    const types = []
    if (props.type.length > 0) {
        if (props.type === "vergaderingen") types.push("vergadering")
        else types.push(props.type)
    }
    const years = []
    if (props.year.length > 0) {
        years.push(props.year)
    }
    const speakers = []
    if (props.speaker.length > 0) {
        speakers.push(props.speaker)
    }
    const videos = []
    if (props.video.length > 0) {
        videos.push(props.video)
    }

    const weaviateOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            collection: "TranscriptsV2",
            query: searchQuery.value,
            limit: props.limit,
            target_vec: "text",
            government: gemeentes,
            meetingType: types,
            year: years,
            speaker: speakers,
            video: videos,
        })
    };
    console.log(weaviateOptions)
    const weaviateResponse = await fetch(`http://127.0.0.1:3012/api/weaviate/searchBM25`, weaviateOptions)
    const weaviateData = await weaviateResponse.json();
    searchResults.value = weaviateData.objects
    console.log(weaviateData)
}

async function vectorSearch() {
    const embedOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: [searchQuery.value] })
    };
    console.log(embedOptions)
    const embedResponse = await fetch(`http://127.0.0.1:3012/api/embed`, embedOptions)
    const embedData = await embedResponse.json();
    const embedVector = embedData["embeddings"][0]

    const gemeentes = []
    if (props.gemeente.length > 0) {
        gemeentes.push(props.gemeente)
    }
    const types = []
    if (props.type.length > 0) {
        if (props.type === "vergaderingen") types.push("vergadering")
        else types.push(props.type)
    }
    const years = []
    if (props.year.length > 0) {
        years.push(props.year)
    }
    const speakers = []
    if (props.speaker.length > 0) {
        speakers.push(props.speaker)
    }
    const videos = []
    if (props.video.length > 0) {
        videos.push(props.video)
    }

    const weaviateOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            collection: "TranscriptsV2",
            vector: embedVector,
            limit: props.limit,
            target_vec: "text",
            government: gemeentes,
            meetingType: types,
            year: years,
            speaker: speakers,
            video: videos,
        })
    };
    const weaviateResponse = await fetch(`http://127.0.0.1:3012/api/weaviate/searchVector`, weaviateOptions)
    const weaviateData = await weaviateResponse.json();
    searchResults.value = weaviateData.objects
    console.log(weaviateData)
}

async function hybridSearch() {
    const embedOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: [searchQuery.value] })
    };
    console.log(embedOptions)
    const embedResponse = await fetch(`http://127.0.0.1:3012/api/embed`, embedOptions)
    const embedData = await embedResponse.json();
    const embedVector = embedData["embeddings"][0]

    const gemeentes = []
    if (props.gemeente.length > 0) {
        gemeentes.push(props.gemeente)
    }
    const types = []
    if (props.type.length > 0) {
        if (props.type === "vergaderingen") types.push("vergadering")
        else types.push(props.type)
    }
    const years = []
    if (props.year.length > 0) {
        years.push(props.year)
    }
    const speakers = []
    if (props.speaker.length > 0) {
        speakers.push(props.speaker)
    }
    const videos = []
    if (props.video.length > 0) {
        videos.push(props.video)
    }
    console.log(props.alpha)
    const weaviateOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            collection: "TranscriptsV2",
            query: searchQuery.value,
            vector: embedVector,
            limit: props.limit,
            alpha: props.alpha,
            target_vec: "text",
            government: gemeentes,
            meetingType: types,
            year: years,
            speaker: speakers,
            video: videos,
        })
    };
    const weaviateResponse = await fetch(`http://127.0.0.1:3012/api/weaviate/searchHybrid`, weaviateOptions)
    const weaviateData = await weaviateResponse.json();
    searchResults.value = weaviateData.objects
    console.log(weaviateData)
}

async function clickSearch() {
    console.log(`Clicked search with method ${props.method} and limit ${props.limit}. Current search parameters: gemeente: ${props.gemeente}, type: ${props.type}, year: ${props.year}, speaker: ${props.speaker}, video: ${props.video}`)
    if (searchQuery.value == "") {
        return
    }
    if (props.method == "vector") {
        await vectorSearch()
    } else if (props.method == "bm25") {
        await vectorBM25()
    } else if (props.method == "hybrid") {
        await hybridSearch() // TODO idk of dit helemaal goed werktx
    }

    emit("newQuery", searchQuery.value)
}

</script>

<template>

    <div class="max-w-md mx-auto">
        <label for="default-search"
            class="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white">Search</label>
        <div class="relative">
            <div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
                <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" />
                </svg>
            </div>
            <input type="search" id="default-search" :value="searchQuery"
                @input="event => searchQuery = event.target.value" @keydown.enter="clickSearch"
                class="block w-96 p-4 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                placeholder="Wetgeving betaald parkeren" required />
            <button @click="clickSearch"
                class="text-white absolute end-2.5 bottom-2.5 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Search</button>
        </div>
    </div>

</template>
