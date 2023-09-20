<template>
    <div id="create-trade">
        <div class="container-fluid">
            <div class="card p-3">
                <div class="card-body">
                    <form class="mx-auto" @submit.prevent="submitFormData">
                        <h1 class="display-6">Add Trade</h1>
                        <hr>
                        <p class="text-secondary small">Add a new trade by entering the trade details below.</p>
                        <div class="form-floating mb-3">
                            <input v-model.number="formData.amountOfSharesBought" type="number" class="form-control"
                                id="amountOfSharesBought" step="any">

                            <label for="amountOfSharesBought" class="form-label">Amount of Shares Bought</label>
                            <span
                                v-if="errorMessage && errorMessage.amount_of_shares_bought && errorMessage.amount_of_shares_bought[0] !== null"
                                class="text-danger">{{ errorMessage.amount_of_shares_bought[0] }}</span>
                        </div>
                        <div class="form-floating mb-3">
                            <select v-model="formData.symbol" class="form-select" id="symbol">
                                <option v-for="(choice, value) in SYMBOL_CHOICES" :key="value" :value="value">{{ choice }}
                                </option>
                            </select>
                            <label for="symbol" class="form-label">Symbol</label>
                            <span
                                v-if="errorMessage && errorMessage.symbol_of_shares && errorMessage.symbol_of_shares[0] !== null"
                                class="text-danger">{{ errorMessage.symbol_of_shares[0] }}</span>
                        </div>
                        <div class="form-floating mb-3">
                            <select v-model="formData.buyOrSell" class="form-select" id="buyOrSell">
                                <option v-for="(choice, value) in BUY_SELL_CHOICES" :key="value" :value="value">{{ choice }}
                                </option>
                            </select>
                            <label for="buyOrSell" class="form-label">Buy / Sell</label>
                            <span v-if="errorMessage && errorMessage.buy_sell && errorMessage.buy_sell[0] !== null"
                                class="text-danger">{{ errorMessage.buy_sell[0] }}</span>
                        </div>
                        <div class="form-floating mb-3">
                            <input v-model.number="formData.pricePerShare" type="number" class="form-control"
                                id="pricePerShare">
                            <span
                                v-if="errorMessage && errorMessage.price_per_share && errorMessage.price_per_share[0] !== null"
                                class="text-danger">{{ errorMessage.price_per_share[0] }}</span>
                            <label for="pricePerShare" class="form-label">Price per Share</label>
                        </div>
                        <button type="submit" class="btn btn-primary">Add Trade</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script>
import { createTrade } from '../../services/api.js';

export default {
    name: 'CreateTrade',
    data() {
        return {
            formData: {
                amountOfSharesBought: null,
                symbol: '',
                buyOrSell: '',
                quantity: null,
                pricePerShare: '',
            },
            response: '',
            errorMessage: {},
            token: this.$store.state.token,
        };
    },
    methods: {
        async clearFormData() {
            this.formData.amountOfSharesBought = null;
            this.formData.symbol = '';
            this.formData.buyOrSell = null;
            this.formData.quantity = '';
            this.formDate.pricePerShare = '';
            this.errorMessage = '';
        },
        async submitFormData(e) {
            e.preventDefault();
            this.errorMessage = '';
            try {
                const response = await createTrade({
                    amount_of_shares_bought: this.formData.amountOfSharesBought,
                    symbol_of_shares: this.formData.symbol,
                    buy_sell: this.formData.buyOrSell,
                    quantity: this.formData.quantity,
                    price_per_share: this.formData.pricePerShare,
                });
                this.$router.push('/trades');
            }
            catch (error) {
                this.errorMessage = error.response.data;
            }
        },
    },
    computed: {
        SYMBOL_CHOICES() {
            return {
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
                'Buy': 'Buy',
                'Sell': 'Sell',
            }
        }
    },
};
</script>
  
<style>
#create-trade {
    max-width: 800px;
    width: 100%;
}

#create-trade .container-fluid form {
    width: 100%;
    max-width: 777px;
}
</style>
  