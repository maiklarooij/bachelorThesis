<script setup>

defineProps({
    gemeente: String,
    num_vids: Number,
})

</script>

<template>

    <div class="flex flex-col justify-center min-w-40 min-h-40  p-3 bg-slate-700 hover:bg-slate-600">
        <div class="my-1">
            {{ gemeente }}
        </div>
        <div class="my-1">
            Total videos: {{ num_vids }}
        </div>

    </div>

</template>
