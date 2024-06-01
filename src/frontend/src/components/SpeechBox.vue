<script setup>
import { ref } from "vue";

const props = defineProps({
    role: String,
    message: String,
    visible: Boolean,
})

function getRoleClass() {
    if (props.role === "user") {
        return "bg-amber-600 ml-auto mr-10"
    } else if (props.role === "assistant") {
        return "bg-blue-600 mr-auto ml-10"
    }
}

function processedMessage(m) {
    // Find the index of 'context:'
    const contextIndex = m.indexOf('Context:');

    // If 'context:' is found, return the substring before it
    if (contextIndex !== -1) {
        return m.substring(0, contextIndex);
    } else {
        // If 'context:' is not found, return the original message
        return m;
    }
}

</script>

<template>
    <div v-if="visible" class="flex max-w-96 p-2 rounded text-left" :class="getRoleClass()">
        {{ processedMessage(message) }}
    </div>

</template>