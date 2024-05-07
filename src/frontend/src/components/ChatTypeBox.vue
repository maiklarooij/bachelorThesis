<script setup>
import { ref } from "vue"

const chatQuery = ref("")

const emit = defineEmits(["askQuestion"])

function clickAsk() {
    if (chatQuery.value == "") return
    emit("askQuestion", chatQuery.value)
    chatQuery.value = ""
}

</script>

<template>

    <div class="max-w-md mx-auto">
        <label for="default-search"
            class="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white">Search</label>
        <div class="relative">
            <input type="search" id="default-search" :value="chatQuery" @input="event => chatQuery = event.target.value"
                @keydown.enter="clickAsk" style="width: 420px;"
                class="block p-4 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                placeholder="Wat zei Groenlinks over betaald parkeren?" required />
            <button @click="clickAsk"
                class="text-white absolute end-2.5 bottom-2.5 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Ask</button>
        </div>
    </div>

</template>
