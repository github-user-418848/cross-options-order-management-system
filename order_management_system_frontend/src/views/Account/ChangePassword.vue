<template>
    <div id="change-password" class="container-fluid mt-5">
        <div class="alert alert-dismissible fade show" :class="alertType" role="alert" v-if="alertMessage">
            {{ alertMessage }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        <div class="card p-3">
            <div class="card-body">
                <h1 class="display-6">Change Password</h1>
                <hr>
                <p class="text-secondary small">Change your password securely by filling out the form below.</p>
                <form @submit.prevent="handleChangePassword">
                    <div class="form-floating mb-3">
                        <input type="password" class="form-control" id="currentPassword" v-model="currentPassword">
                        <label for="currentPassword" class="form-label">Current Password</label>
                        <span
                            v-if="errorMessage && errorMessage.current_password && errorMessage.current_password[0] !== null"
                            class="text-danger">{{ errorMessage.current_password[0] }}</span>
                    </div>
                    <div class="form-floating mb-3">
                        <input type="password" class="form-control" id="newPassword" v-model="newPassword">
                        <label for="newPassword" class="form-label">New Password</label>
                        <span v-if="errorMessage && errorMessage.new_password && errorMessage.new_password[0] !== null"
                            class="text-danger">{{ errorMessage.new_password[0] }}</span>
                    </div>
                    <div class="form-floating mb-3">
                        <input type="password" class="form-control" id="confirmPassword" v-model="confirmPassword">
                        <label for="confirmPassword" class="form-label">Confirm New Password</label>
                        <span
                            v-if="errorMessage && errorMessage.confirm_new_password && errorMessage.confirm_new_password[0] !== null"
                            class="text-danger">{{ errorMessage.confirm_new_password[0] }}</span>
                    </div>
                    <span v-if="errorMessage && errorMessage.non_field_errors && errorMessage.non_field_errors[0] !== null"
                        class="text-danger">{{ errorMessage.non_field_errors[0] }}</span>
                    <div class="text-center">
                        <button type="submit" class="btn btn-primary">Change Password</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>
  
  
<script>
import { changePassword } from '../../services/api';

export default {
    name: 'ChangePassword',
    data() {
        return {
            currentPassword: '',
            newPassword: '',
            confirmPassword: '',
            alertType: null,
            alertMessage: null,
            errorMessage: null,
        }
    },
    methods: {
        async handleChangePassword() {
            try {
                // Call the changePassword API function with the current and new passwords
                const response = await changePassword({
                    current_password: this.currentPassword,
                    new_password: this.newPassword,
                    confirm_new_password: this.confirmPassword,
                });

                if (response.data.message === "Password changed successfully") {
                    this.currentPassword = '';
                    this.newPassword = '';
                    this.confirmPassword = '';
                    this.alertType = "alert-success";
                    this.alertMessage = response.data.message;
                } else {
                    this.message = 'Password change failed. Please check your input.';
                    this.toastTitle = "Error";
                    this.alertType = "alert-warning";
                    this.alertMessage = response.data.message;
                }
            } catch (error) {
                this.errorMessage = error.response.data;
                // console.error('Error changing password:', );
                this.error = 'An error occurred while changing the password.';
            }
        },
    },
}
</script>
<style>
#change-password {
    max-width: 700px;
    width: 100%;
}
</style>