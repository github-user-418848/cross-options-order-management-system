<template>
    <div id="registration" class="mx-auto">
        <div class="card">
            <div class="card-body">
                <h1 class="display-6">Registration</h1>
                <hr>
                <p class="text-secondary small">Create a new account by filling out the form below.</p>
                <form class="mx-auto" @submit.prevent="submitFormData">
                    <div class="row mx-auto">
                        <div class="col-md-8">
                            <div class="form-floating form-group">
                                <input class="form-control" v-model="name" type="text" id="name" />
                                <label class="small" for="name">Name</label>
                                <span v-if="errorMessage && errorMessage.name && errorMessage.name[0] !== null"
                                    class="text-danger">{{ errorMessage.name[0] }}</span>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="form-floating form-group">
                                <input class="form-control" v-model="age" type="number" id="age" />
                                <label class="small" for="age">Age</label>
                                <span v-if="errorMessage && errorMessage.age && errorMessage.age[0] !== null"
                                    class="text-danger">{{ errorMessage.age[0] }}</span>
                            </div>
                        </div>
                        <div class="col-md-12">
                            <div class="form-floating form-group">
                                <input class="form-control" v-model="email" type="email" id="email" />
                                <label class="small" for="email">Email</label>
                                <span v-if="errorMessage && errorMessage.email && errorMessage.email[0] !== null"
                                    class="text-danger">{{ errorMessage.email[0] }}</span>
                            </div>
                        </div>
                        <div class="col-md-12">
                            <div class="form-floating form-group">
                                <input class="form-control" v-model="username" type="text" id="username" />
                                <label class="small" for="username">Username</label>
                                <span v-if="errorMessage && errorMessage.username && errorMessage.username[0] !== null"
                                    class="text-danger">{{ errorMessage.username[0] }}</span>
                            </div>
                        </div>
                        <div class="col-md-12">
                            <div class="form-floating form-group">
                                <input class="form-control" v-model="password" type="password" id="password" />
                                <label class="small" for="password">Password</label>
                                <span v-if="errorMessage && errorMessage.password && errorMessage.password[0] !== null"
                                    class="text-danger">{{ errorMessage.password[0] }}</span>
                            </div>
                        </div>
                        <div class="d-flex justify-content-center align-items-center flex-column">
                            <div class="g-recaptcha" :data-sitekey="recaptchaSiteKey"></div>
                            <span v-if="errorMessage" class="text-danger">{{ errorMessage }}</span>
                        </div>
                    </div>
                    <input type="submit" class="btn btn-primary d-block" name="submit" value="Register" />
                </form>
                <hr>
                <p class="small text-center">Already have an account? <router-link class="text-decoration-none text-secondary" to="/login">Login here</router-link></p>
            </div>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';
import { register } from '../../services/api.js';

export default {

    name: 'Register',
    data() {
        return {
            basePath: import.meta.env.VITE_BACKEND_BASE_PATH,
            recaptchaSiteKey: import.meta.env.VITE_RECAPTCHA_SITE_KEY,
            email: ref(''),
            username: ref(''),
            name: ref(''),
            age: ref(null),
            password: ref(''),
            errorMessage: ref(''),
        };
    },
    mounted() {
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
            this.name = '';
            this.age = '';
            this.email = '';
            this.password = '';
            grecaptcha.reset();
        },
        async submitFormData(e) {
            e.preventDefault();
            this.errorMessage = '';

            const recaptchaResponse = grecaptcha.getResponse();
            if (!recaptchaResponse) {
                this.errorMessage = 'reCAPTCHA verification failed';
                return;
            }

            try {
                const response = await register({
                    username: this.username,
                    password: this.password,
                    email: this.email,
                    name: this.name,
                    age: this.age,
                    'g-recaptcha-response': recaptchaResponse
                });
                this.$router.push('/login');
            } catch (error) {
                this.errorMessage = error.response.data;
            }
        },
    },
};
</script>
<style scoped>
#registration {
    max-width: 900px;
    width: 100%;
}

#registration .card {
    padding: 15px;
}

#registration .form-group,
#registration .g-recaptcha {
    margin-bottom: 20px;
}

#registration .btn {
    max-width: 220px;
    width: 100%;
    margin: 0 auto;
}

#registration center {
    position: relative;
}

#registration .g-recaptcha {
    transform: scale(0.9);
}

@media screen and (max-width: 370px) {
    #registration .g-recaptcha {
        display: flex;
        justify-content: center;
        left: 50%;
        top: 50%;
        transform: scale(0.75);
    }
}
</style>
  