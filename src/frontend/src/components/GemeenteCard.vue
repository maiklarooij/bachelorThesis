<script setup>

const emit = defineEmits(["clicked"])

defineProps({
    gemeente: String,
    num_vids: Number,
})

function handleClick() {
    emit("clicked")
}

</script>

<template>

    <div class="flex flex-col p-3 ">
        <div>
            <div @click="handleClick" style="color: #99c3ff;" class=" hover:underline font-bold text-lg my-1">
                Gemeente {{ gemeente }}
            </div>
            <div class="my-1">
                Total videos: {{ num_vids }}
            </div>
        </div>
    </div>

</template>
