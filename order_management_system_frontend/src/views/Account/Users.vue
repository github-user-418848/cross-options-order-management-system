<template>
    <div id="dashboard">
        <div class="d-flex align-items-center justify-content-md-between flex-md-row flex-column justify-content-center">
            <h1 class="display-6">Users</h1>
        </div>
        <hr>
        <p class="text-secondary small">View and manage user details below.</p>
        <div class="container-fluid">
            <template v-if="loggedIn">
                <div v-if="currentPage === 1" class="row justify-content-md-start px-0 justify-content-center">
                    <div class="col-md-4">
                        <div class="form-floating mb-3">
                            <input class="form-control" type="input" id="keyword" v-model="keyword" @keyup="applyFilters" />
                            <label for="keyword">Keyword</label>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <div class="form-floating mb-3">
                            <select v-model="age" class="form-select" id="age" @change="applyFilters">
                                <option value="">All</option>
                                <option v-for="age in 53" :key="age" :value="age + 18">{{ age + 18 }}</option>
                            </select>
                            <label for="age">Age</label>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="form-floating mb-3">
                            <input class="form-control" type="date" id="startDate" v-model="startDate"
                                @change="applyFilters" />
                            <label for="startDate">Start Date</label>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="form-floating mb-3">
                            <input class="form-control" type="date" id="endDate" v-model="endDate" @change="applyFilters" />
                            <label for="endDate">End Date</label>
                        </div>
                    </div>
                </div>
                <template v-if="users !== null && users.count != 0">
                    <DynamicTable :caption="tableCaptionWithPage" :headers="tableHeaders" :items="users.results" />
                    <nav aria-label="Page navigation" v-if="totalPages > 1">
                        <ul class="pagination justify-content-center">
                            <li class="page-item" :class="{ disabled: currentPage === 1 }">
                                <button class="page-link" @click="goToPage(currentPage - 1)">Previous</button>
                            </li>
                            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                                <button class="page-link" @click="goToPage(currentPage + 1)">Next</button>
                            </li>
                        </ul>
                    </nav>
                </template>
            </template>
            <template v-else>
                <p class="d-flex align-items-center justify-content-center vh-100 my-auto border rounded">No data found.</p>
            </template>
        </div>
    </div>
</template>
<script>

import { ref } from 'vue';
import { getUsers } from '../../services/api.js';
import DynamicTable from '../../components/DynamicTable.vue';

export default {
    name: 'Dashboard',
    components: {
        DynamicTable,
    },
    data() {
        const currentDate = this.currentDate;

        return {
            tableCaption: 'List of Users',
            tableHeaders: [
                { key: "id", label: "ID" },
                { key: "email", label: "Email" },
                { key: "username", label: "Username" },
                { key: "name", label: "Name" },
                { key: "age", label: "Age" },
                { key: "is_active", label: "Active" },
                { key: "is_staff", label: "Staff" },
                { key: "date_joined", label: "Date Joined" },
            ],
            users: ref(null),
            createTrade: '/users/add',
            loggedIn: this.$store.state.loggedIn,
            token: this.$store.state.token,
            currentPage: 1,
            totalPages: 1,
            keyword: '',
            age: '',
            startDate: currentDate,
            endDate: currentDate,
        };
    },
    async mounted() {
        if (this.loggedIn) {
            this.applyFilters();
        }
    },
    computed: {
        tableCaptionWithPage() {
            return `${this.tableCaption} - Page ${this.currentPage} of ${this.totalPages}`;
        },
    },
    methods: {
        async applyFilters() {
            await this.loadUsers();
            await this.loadUserTrades();
        },
        async loadUsers() {
            try {
                this.users = await getUsers(this.currentPage, this.age, this.startDate, this.endDate, this.keyword);
                this.totalPages = Math.ceil(this.users.count / 10);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        },
        formatDate(dateString) {
            const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
            return new Date(dateString).toLocaleDateString(undefined, options);
        },
        goToPage(page) {
            if (page >= 1 && page <= this.totalPages) {
                this.currentPage = page;
                this.loadUsers();
            }
        },
    }
};
</script>