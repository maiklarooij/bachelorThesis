<script setup>

defineProps({
    gemeente: String,
    type: String,
})

</script>

<template>

    <div class="flex flex-col min-w-10 min-h-10 bg-slate-700 p-3">
        <div>
            {{ type }}
        </div>
    </div>

</template>
