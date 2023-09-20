<template>
    <footer class="border-top">
        <div class="container-fluid text-center text-gray small py-3">
            Order Management System {{ currentYear }}
        </div>
    </footer>
</template>
<script>
export default {
    name: 'Footer',
    data() {
        return {
            currentYear: new Date().getFullYear(), // Get the current year
        };
    },
}
</script>