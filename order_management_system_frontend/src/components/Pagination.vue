<template>
    <nav aria-label="Page navigation">
        <ul class="pagination justify-content-center">
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <button class="page-link" @click="changePage(currentPage - 1)">Previous</button>
            </li>
            <li class="page-item" v-for="page in pages" :key="page" :class="{ active: page === currentPage }">
                <button class="page-link" @click="changePage(page)">{{ page }}</button>
            </li>
            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                <button class="page-link" @click="changePage(currentPage + 1)">Next</button>
            </li>
        </ul>
    </nav>
</template>
<script>
export default {
    props: {
        currentPage: Number,
        totalPages: Number,
    },
    computed: {
        pages() {
            const startPage = Math.max(1, this.currentPage - 2);
            const endPage = Math.min(this.totalPages, startPage + 4);

            return Array.from({ length: endPage - startPage + 1 }, (_, i) => startPage + i);
        },
    },
    methods: {
        changePage(page) {
            if (page >= 1 && page <= this.totalPages) {
                this.$emit('page-change', page);
            }
        },
    },
};
</script>
  