<script setup>

defineProps({
    gemeente: String,
    type: String,
})

</script>

<template>

    <div style="color: #99c3ff;" class=" hover:underline font-bold text-lg my-1">
        <div>
            {{ type }}
        </div>
    </div>

</template>
