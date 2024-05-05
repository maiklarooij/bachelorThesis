<script setup>

defineProps({
    gemeente: String,
    type: String,
})

</script>

<template>

    <div class="text-blue-300 hover:underline font-bold text-lg my-1">
        <div>
            {{ type }}
        </div>
    </div>

</template>
