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

</script>

<template>
    <div v-if="visible" class="flex max-w-96 p-2 rounded" :class="getRoleClass()">
        {{ message }}
    </div>

</template>