<template>
    <div id="dashboard">
        <div class="d-flex align-items-center justify-content-md-between flex-md-row flex-column justify-content-center">
            <h1 class="display-6">Trades Summary</h1>
            <router-link class="btn btn-primary" :to="createTrade">Create New Trade</router-link>
        </div>
        <hr>
        <p class="text-secondary small">View a summary of trades and apply filters to narrow down the results.</p>
        <div class="container-fluid">
            <template v-if="loggedIn">
                <div v-if="currentPage === 1" class="row justify-content-md-start px-0 justify-content-center">
                    <div class="col-md-3">
                        <div class="form-floating mb-3">
                            <select v-model="symbol" class="form-select" id="symbol" @change="applyFilters">
                                <option v-for="(choice, value) in SYMBOL_CHOICES" :key="value" :value="value">{{ choice }}
                                </option>
                            </select>
                            <label for="symbol">Symbol</label>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="form-floating mb-3">
                            <select v-model="buyOrSell" class="form-select" id="buyOrSell" @change="applyFilters">
                                <option v-for="(choice, value) in BUY_SELL_CHOICES" :key="value" :value="value">{{ choice }}
                                </option>
                            </select>
                            <label for="buyOrSell">Buy / Sell</label>
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
                <template v-if="trades !== null && trades.count != 0">
                    <DynamicTable :caption="tableCaptionWithPage" :headers="tableHeaders" :items="trades.results" />
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
                <template v-else>
                    <p class="d-flex align-items-center justify-content-center vh-100 my-auto border rounded">No data found.
                    </p>
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
import { getTrades } from '../../services/api.js';
import DynamicTable from '../../components/DynamicTable.vue';

export default {
    name: 'Summary',
    components: {
        DynamicTable,
    },
    data() {
        const currentDate = this.currentDate;

        return {
            tableCaption: "List of Historical Trades",
            tableHeaders: [
                { key: "id", label: "ID" },
                { key: "date_of_execution", label: "Date" },
                { key: "amount_of_shares_bought", label: "Amount of Shares Bought" },
                { key: "symbol_of_shares", label: "Symbol" },
                { key: "buy_sell", label: "Buy/Sell" },
                { key: "price_per_share", label: "Price per Share" },
                { key: "user", label: "User ID" },
                { key: "total_amount_paid", label: "Total Amount" },
                { key: "actions", label: "Actions" }
            ],
            trades: ref(null),
            createTrade: '/trades/add',
            loggedIn: this.$store.state.loggedIn,
            token: this.$store.state.token,
            currentPage: 1,
            totalPages: 1,
            startDate: currentDate,
            endDate: currentDate,
            symbol: '',
            buyOrSell: '',
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
        currentDate() {
            const today = new Date();
            const year = today.getFullYear();
            const month = String(today.getMonth() + 1).padStart(2, '0');
            const day = String(today.getDate()).padStart(2, '0');
            return `${year}-${month}-${day}`;
        },
        SYMBOL_CHOICES() {
            return {
                '': 'All',
                'AAPL': 'Apple Inc. (Stock)',
                'GOOGL': 'Alphabet Inc. (Google) (Stock)',
                'MSFT': 'Microsoft Corporation (Stock)',
                'SPY': 'SPDR S&P 500 ETF Trust (ETF)',
                'QQQ': 'Invesco QQQ Trust (ETF)',
                'GLD': 'SPDR Gold Trust (ETF)',
                'BTC': 'Bitcoin (Cryptocurrency)',
                'ETH': 'Ethereum (Cryptocurrency)',
                'XRP': 'Ripple (Cryptocurrency)',
                'EUR/USD': 'Euro/US Dollar (Forex)',
                'GBP/JPY': 'British Pound/Japanese Yen (Forex)',
                'USD/JPY': 'US Dollar/Japanese Yen (Forex)',
                'XAU': 'Gold (Commodity)',
                'CL': 'Crude Oil (Commodity)',
                'NG': 'Natural Gas (Commodity)',
                'SPX': 'S&P 500 Index Options (Options/Futures)',
                'ES': 'E-Mini S&P 500 Futures (Options/Futures)',
                'TLT': 'iShares 20+ Year Treasury Bond ETF (Bond)',
                'AGG': 'iShares Core U.S. Aggregate Bond ETF (Bond)',
                'DJI': 'Dow Jones Industrial Average (Index)',
                'IXIC': 'Nasdaq Composite Index (Index)',
                'S&P 500': 'Standard & Poor\'s 500 Index (Index)',
                'VTSAX': 'Vanguard Total Stock Market Index Fund (Mutual Fund)',
                'FBGRX': 'Fidelity Blue Chip Growth Fund (Mutual Fund)',
            };
        },
        BUY_SELL_CHOICES() {
            return {
                '': 'All',
                'Buy': 'Buy',
                'Sell': 'Sell',
            }
        }
    },
    methods: {
        formatDate(dateString) {
            const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
            return new Date(dateString).toLocaleDateString(undefined, options);
        },
        applyFilters() {
            this.loadTrades();
        },
        async loadTrades() {
            try {
                this.trades = await getTrades(this.currentPage, this.startDate, this.endDate, this.buyOrSell, this.symbol);
                this.trades.results.forEach((trade) => {
                    trade.updateLink = `/trades/${trade.id}/update`; // Add this line
                });
                this.totalPages = Math.ceil(this.trades.count / 10);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        },
        goToPage(page) {
            if (page >= 1 && page <= this.totalPages) {
                this.currentPage = page;
                this.loadTrades();
            }
        },
    }
};
</script>
<style>
#dashboard {
    max-width: 1200px;
    width: 100%;
}

#dashboard .container-fluid {
    min-height: 100vh;
}
</style>
  