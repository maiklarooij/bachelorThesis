<script setup>
import ResultCard from './ResultCard.vue';

defineProps({
    query: String,
    results: Array,
})

</script>

<template>
    <ResultCard v-for="r in results" :query="query"  :code="r.properties.code" :text="r.properties.text"
        :start="r.properties.start" :end="r.properties.end" :year="r.properties.year"
        :government="r.properties.government" :type="r.properties.type" :speaker="r.properties.speaker"
        :distance="r.distance">
    </ResultCard>
    <span v-if="results.length == 0">No search results</span>
</template>
