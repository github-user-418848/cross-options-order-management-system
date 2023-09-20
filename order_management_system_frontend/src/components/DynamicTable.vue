<template>
    <div class="table-responsive">
        <table class="table table-hover table-lg border align-middle caption-top">
            <caption class="small">{{ caption }}</caption>
            <thead>
                <tr class="align-middle text-nowrap">
                    <th v-for="header in headers" :key="header.key">
                        <!-- Conditionally render the "Action" column header -->
                        <template v-if="header.key !== 'actions' || isAdmin">
                            {{ header.label }}
                        </template>
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="item in items" :key="item.id">
                    <td v-for="(header, index) in headers" :key="header.key">
                        <router-link class="text-decoration-none" v-if="header.key === 'actions' && isAdmin" :to="'/trades/update/' + item.id">Update</router-link>
                        <!-- Use item[header.key] to access item data dynamically -->
                        <span v-if="index !== 7">
                            {{ item[header.key] }}
                        </span>
                        <span v-else
                            :class="{ 'text-danger': item[header.key] < 0, 'text-success': item[header.key] >= 0 }">
                            {{ item[header.key] }}
                        </span>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
  
<script>
import { useStore } from 'vuex';

export default {
    name: 'DynamicTable',
    props: {
        caption: String,      // Caption for the table
        headers: Array,       // Array of header objects { key, label }
        items: Array          // Array of data items
    },
    computed: {
        isAdmin() {
            const store = useStore();
            return (store.state.isSuperUser || store.state.isStaff);
        },
    }
};
</script>
  
<style scoped>
#dashboard .table td {
    padding: clamp(0.5rem, 0.5rem + 0.625vw, 1.25rem);
}
</style>
  