<script setup>

defineProps({
    gemeente: String,
    type: String,
})

</script>

<template>

    <div class=" mb-1 mt-2">
        <div class="text-blue-300 hover:underline font-bold text-lg">
            {{ type }}
        </div>
        <!-- <div>
        </div> -->
    </div>

</template>
