<template>
    <div id="profile" class="container-fluid">
        <div class="card p-3">
            <div class="card-body">
                <h1 class="display-6">My Account</h1>
                <hr>
                <p class="text-secondary small">View and manage your account details below.</p>
                <div class="row align-items-center mx-auto justify-content-center justify-content-between">
                    <div class="d-flex flex-md-row flex-column align-items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" width="250" height="250" fill="currentColor"
                            class="bi bi-person-circle img-fluid me-0 me-md-5" viewBox="0 0 16 16">
                            <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z" />
                            <path fill-rule="evenodd"
                                d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z" />
                        </svg>
                        <span class="text-center text-md-start">
                            <h2>{{ profile.name }}</h2>
                            <p class="small fst-italic">Joined since {{ profile.date_joined }}</p>
                            <p class=""><strong>ID No.</strong> {{ profile.id }}</p>
                            <p class=""><strong>Username</strong> {{ profile.username }}</p>
                            <p class=""><strong>Email</strong> {{ profile.email }}</p>
                            <p><strong>Age</strong> {{ profile.age }}</p>
                        </span>
                    </div>
                    <!-- <div class="col-lg-4 col-md-12 text-md-end text-center">
                        <a href="/change_password" class="btn btn-primary">Change Password</a>
                    </div> -->
                </div>
            </div>
        </div>
        
        <a href="/change_password" class="btn btn-primary mt-3 d-flex justify-content-center">Change Password</a>
        <a href="/logout" class="btn btn-outline-danger mt-3 d-flex justify-content-center">Logout</a>

    </div>
</template>
  
<script>
import { getProfile } from '../../services/api';

export default {
    name: 'MyAccount',
    data() {
        return {
            profile: null,
        }
    },
    async created() {
        try {
            this.profile = await getProfile();
        } catch (error) {
            console.error('Error fetching profile:', error);
        }
    },
}
</script>
<style>
#profile {
    max-width: 1000px;
    width: 100%;
}
</style>