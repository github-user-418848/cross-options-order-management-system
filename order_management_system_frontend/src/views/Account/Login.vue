<template>
    <div id="login" class="mx-auto">
        <div class="card">
            <h2 class="text-center">Login</h2>
            <div class="card-body">
                <form class="mx-auto" @submit.prevent="login">
                    <div class="form-floating form-group">
                        <input class="form-control" v-model="username" type="text" id="username" />
                        <label class="small" for="username">Username</label>
                        <span v-if="errorMessage && errorMessage.username && errorMessage.username[0] !== null"
                            class="text-danger">{{ errorMessage.username[0] }}</span>
                    </div>
                    <div class="form-floating form-group">
                        <input class="form-control" v-model="password" type="password" id="password" />
                        <label class="small" for="password">Password</label>
                        <span v-if="errorMessage && errorMessage.password && errorMessage.password[0] !== null"
                            class="text-danger">{{ errorMessage.password[0] }}</span>
                    </div>
                    <div class="d-flex justify-content-center align-items-center flex-column">
                        <div class="g-recaptcha" :data-sitekey="recaptchaSiteKey"></div>
                        <span v-if="errorMessage" class="text-danger">{{ errorMessage }}</span>
                    </div>
                    <input type="submit" class="btn btn-primary d-block" name="submit" value="Login" />
                    <hr>
                    <p class="text-center small">Don't have an account? Feel free to <a class="text-decoration-none text-secondary" href="/register">Sign Up</a> here.</p>
                </form>
            </div>
        </div>
    </div>
</template>
<script>
import { ref } from 'vue';

export default {
    name: 'Login',
    data() {
        return {
            basePath: import.meta.env.VITE_BACKEND_BASE_PATH,
            recaptchaSiteKey: import.meta.env.VITE_RECAPTCHA_SITE_KEY,
            username: ref(''),
            password: ref(''),
            errorMessage: ref(''),
        };
    },
    async mounted() {
        this.loadRecaptchaScript();
    },
    methods: {
        async loadRecaptchaScript() {
            const script = document.createElement('script');
            script.src = 'https://www.google.com/recaptcha/api.js';
            script.async = true;
            script.defer = true;
            script.onload = this.initializeRecaptcha;
            document.head.appendChild(script);
        },
        async clearFormData() {
            this.username = '';
            this.password = '';
            grecaptcha.reset();
        },
        async login(e) {
            e.preventDefault();
            this.errorMessage = '';
            if (typeof grecaptcha === 'undefined' || grecaptcha === null) {
                this.errorMessage = 'reCAPTCHA script was not loaded.';
                return;
            }
            const recaptchaResponse = grecaptcha.getResponse();
            if (!recaptchaResponse) {
                this.errorMessage = 'reCAPTCHA verification failed';
                return;
            }
            try {
                this.$store.dispatch('login', {
                    username: this.username,
                    password: this.password,
                    'g-recaptcha-response': recaptchaResponse
                });
            } catch (error) {
                this.errorMessage = error.response.data;
                console.log(this.errorMessage)
            }
        },
    },
};
</script>
<style scoped>
#login {
    max-width: 400px;
    width: 100%;
}

#login .card {
    padding: 15px;
}

#login .form-group,
#login .g-recaptcha {
    margin-bottom: 20px;
}

#login .btn {
    max-width: 220px;
    width: 100%;
    margin: 0 auto;
}

#login center {
    position: relative;
}

#login .g-recaptcha {
    transform: scale(0.9);
}

@media screen and (max-width: 370px) {
    #login .g-recaptcha {
        display: flex;
        justify-content: center;
        left: 50%;
        top: 50%;
        transform: scale(0.75);
    }
}
</style>
  