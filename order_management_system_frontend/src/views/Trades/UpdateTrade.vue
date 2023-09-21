<template>
    <div class="container">
        <div class="alert alert-success alert-dismissible fade show" role="alert" v-if="alertMessage">
            {{ alertMessage }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        <div class="card p-3">
            <div class="card-body">
                <h1 class="display-6">Update Trade</h1>
                <hr>
                <p class="text-secondary small">Update the trade details below.</p>
                <p class="text-secondary small"></p>
                <form @submit.prevent="updateTrade">
                    <div class="d-flex flex-wrap flex-column flex-md-row justify-content-md-between">
                        <div class="col-md-6">User ID Number</div>
                        <div class="col-md-6">
                            <p class="text-start text-md-end">#{{ trade.user }}</p>
                        </div>
                        <div class="col-md-6">Symbol of Shares</div>
                        <div class="col-md-6">
                            <p class="fw-bolder text-start text-md-end">{{ trade.symbol_of_shares }}</p>
                        </div>
                        <div class="col-md-6">Date of Execution</div>
                        <div class="col-md-6">
                            <p class="text-start text-md-end">{{ trade.date_of_execution }}</p>
                        </div>
                        <div class="col-md-6">Buy/Sell</div>
                        <div class="col-md-6">
                            <p class="text-start text-md-end">{{ trade.buy_sell }}</p>
                        </div>
                        <div class="col-md-6">Amount of Shares Bought</div>
                        <div class="col-md-6">
                            <p class="text-start text-md-end">{{ trade.amount_of_shares_bought }}</p>
                        </div>
                        <div class="col-md-6">Price per Share</div>
                        <div class="col-md-6">
                            <p class="text-start text-md-end">{{ trade.price_per_share }}</p>
                        </div>
                    </div>
                    <!-- <hr> -->
                    <div class="form-floating mb-3">
                        <input type="number" class="form-control" v-model="trade.amount_of_shares_bought"
                            id="amount_of_shares_bought" required />
                        <label for="amount_of_shares_bought" class="form-label">Amount of Shares Bought</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input type="number" class="form-control" v-model="trade.price_per_share" id="price_per_share"
                            required />
                        <label for="price_per_share" class="form-label">Price per Share</label>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Update Trade</button>
                </form>
            </div>
        </div>
    </div>
</template>
  
<script>
import { getTradeById, updateTrade } from '../../services/api';
import { ref } from 'vue';

export default {
    name: 'UpdateTrade',
    data() {
        return {
            trade: {
                id: null,
                date_of_execution: '',
                amount_of_shares_bought: null,
                symbol_of_shares: '',
                buy_sell: 'Buy', // Default value
                price_per_share: null,
                user: 1, // You can set this to the logged-in user's ID
            },
            alertMessage: '',
        };
    },
    async mounted() {
        const tradeId = this.$route.params.id;
        await this.loadTradeData(tradeId);
    },
    methods: {
        async loadTradeData(tradeId) {
            try {
                const response = await getTradeById(tradeId);
                this.trade = response;
            } catch (error) {
                console.error('Error loading trade data:', error);
            }
        },
        async updateTrade() {
            try {
                await updateTrade({
                    amount_of_shares_bought: this.trade.amount_of_shares_bought,
                    price_per_share: this.trade.price_per_share,
                }, this.trade.id);
            } catch (error) {
                console.error('Error updating trade:', error);
            }
            this.alertMessage = 'Trade has been updated successfully. Redirecting you back to the trades page.';
            setTimeout(() => {
                this.$router.push('/trades');
            }, 3000);
        },
    },
};
</script>
  
<style scoped>
.container {
    max-width: 500px;
    width: 100%;
    margin: 0 auto;
}
</style>
  