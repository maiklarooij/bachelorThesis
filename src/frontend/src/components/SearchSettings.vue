<script setup>
import { ref, watch } from 'vue';

const emit = defineEmits(['newGemeenteToSearch', 'newMeetingTypeToSearch', 'newMeetingYearToSearch', 'newSpeakerToSearch', 'newSearchMethod', 'newSearchLimit', 'newSearchalpha', 'newAgendaToSearch'])

const props = defineProps({
    gemeentes: Array,
    searchGemeenteActive: Boolean,
    searchTypeActive: Boolean,
    searchYearActive: Boolean,
    availableSpeakersProp: Array,
    availableAgenda: Array,
})

const searchMethod = ref("hybrid");
const searchLimit = ref(10);
const searchalpha = ref(0.5);
const searchGemeente = ref("");
const availableTypes = ref([]);
const searchType     = ref("");
const availableYears = ref([]);
const searchYear     = ref("");
const availableSpeakers = ref([]);
const searchSpeaker     = ref("");
const searchAgenda     = ref("");


watch(searchMethod, (searchMethod, _) => {
    emit("newSearchMethod", searchMethod)
})

watch(searchalpha, (searchalpha, _) => {
    emit("newSearchalpha", searchalpha)
})

watch(searchLimit, (searchLimit, _) => {
    emit("newSearchLimit", searchLimit)
})

watch(searchGemeente, (searchGemeente, _) => {
    fetch(`http://127.0.0.1:3012/api/gemeenteMeetingTypes?gemeente=${searchGemeente}`)
        .then(response => response.json())
        .then(data => availableTypes.value = data.types)

    emit("newGemeenteToSearch", searchGemeente)
})

watch(searchType, (searchType, _) => {
    // console.log(searchType)
    fetch(`http://127.0.0.1:3012/api/gemeenteYears?gemeente=${searchGemeente.value}&meetingType=${searchType}`)
        .then(response => response.json())
        .then(data => availableYears.value = data.years)

    emit("newMeetingTypeToSearch", searchType)
})

watch(searchYear, (searchYear, _) => {
    emit("newMeetingYearToSearch", searchYear)
})

watch(searchSpeaker, (searchSpeaker, _) => {
    emit("newSpeakerToSearch", searchSpeaker)
})

watch(searchAgenda, (searchAgenda, _) => {
    if (!searchAgenda) return
    console.log(searchAgenda)
    const startTime = props.availableAgenda.find(obj => obj.agendaPoint === searchAgenda).start
    const endTime = props.availableAgenda.find(obj => obj.agendaPoint === searchAgenda).start + props.availableAgenda.find(obj => obj.agendaPoint === searchAgenda).time
    console.log(startTime, typeof startTime)
    emit("newAgendaToSearch", startTime, endTime)
})

// function resetSettings() {
//     searchMethod.value = "hybrid"
//     searchLimit.value = 10
//     searchalpha.value = 0.5
//     searchGemeente.value = ""
//     searchType.value = ""
//     searchYear.value = ""
//     searchSpeaker.value = ""
//     searchAgenda.value = ""
// }

</script>

<template>
    <div class="flex gap-x-4 justify-center py-5">

        <!-- search method picker -->
        <select v-model="searchMethod" class="p-2 text-center max-w-28">
            <option value="vector">vector</option>
            <option>bm25</option>
            <option>hybrid</option>
        </select>

        <input v-if="searchMethod === 'hybrid'" type="number" min="0.1" max="1.0" step="0.05" class="px-3 w-20"
            v-model="searchalpha">

        <input type="number" min="1" max="50" step="1" value="1" class="px-3 w-20" v-model="searchLimit">

        <!-- Gemeente picker -->
        <select v-if="searchGemeenteActive" v-model="searchGemeente" class="p-2 text-center max-w-28">
            <option disabled value="">Gemeente</option>
            <option v-for="t in gemeentes">
                {{t.gemeente}}
            </option>
        </select>

        <!-- Type picker -->
        <select v-if="searchTypeActive" v-model="searchType" class="p-2 text-center max-w-28">
            <option disabled value="">Type</option>
            <option v-for="t in availableTypes">
                {{ t.type }}
            </option>

        </select>

        <!-- Year picker -->
        <select v-if="searchYearActive" v-model="searchYear" class="p-2 text-center max-w-28">
            <option disabled value="">Year</option>
            <option v-for="y in availableYears">
                {{ y.year }}
            </option>
        </select>

        <!-- speaker picker -->
        <select v-model="searchSpeaker" class="p-2 text-center max-w-28">
            <option disabled value="">Speaker</option>
            <option v-for="s in availableSpeakersProp">
                {{ s }}
            </option>
        </select>

        <!-- agenda picker -->
        <select v-if="availableAgenda" v-model="searchAgenda" class="p-2 text-center max-w-28">
            <option disabled value="">Agenda</option>
            <option v-for="a in availableAgenda">
                {{ a.agendaPoint }}
            </option>
        </select>

        <!-- <button @click="resetSettings" class="px-2 py-1">Reset</button> -->
    </div>
</template>
