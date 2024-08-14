<template>
    <v-navigation-drawer
        expand-on-hover
        rail
        permanent
    >
        <v-list>
        <v-list-item title="Burning Register">
            <template v-slot:prepend>
                <v-avatar> <v-img src="@/assets/burning_cinema_logo.svg" width=""></v-img> </v-avatar>
            </template>
        </v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-list density="compact" nav>
        <v-list-item prepend-icon="mdi-cash-register" title="Register" value="register" to="/"></v-list-item>
        <v-list-item prepend-icon="mdi-chart-line" title="Statistic" value="statistics" to="/statistics"></v-list-item>
        <v-list-item prepend-icon="mdi-account-cog" title="Admin" value="admin" to="/admin"></v-list-item>
        </v-list>
    </v-navigation-drawer>

  </template>

<script>
export default {
}
</script>

<style>

</style>