<template>
  <v-container>
    <v-row align-center>
      <v-col cols="12" md="6">
        <v-row align-center>
          <v-col cols="4" v-for="d in this.digits" :key="d" class="text-center">
            <v-btn large @click="keyboardValue(d)">{{ d }}</v-btn>
          </v-col>
          <v-col cols="4" class="text-center">
            <v-btn large @click="keyboardValue('delete')">
              <v-icon>mdi-backspace</v-icon>
            </v-btn>
          </v-col>
        </v-row>

      </v-col>
      <v-col>
        <v-btn large color="primary" class="w-100" @click="deleteFromCart()">Delete</v-btn>
        <v-btn large class="w-100" @click="increaseProductAmount()">+</v-btn>
        <v-btn large class="w-100" @click="decreaseProductAmount()">-</v-btn>
        <v-spacer></v-spacer>
        <v-btn large color="success" class="w-100" @click="toggleTeam()">Team</v-btn>
      </v-col>
    </v-row>
    <v-row>
        <v-col>
            <v-btn large color="secondary" class="w-100" @click="clearCart()">Clear all</v-btn>
        </v-col>
        <v-col>
            <v-btn large color="primary" class="w-100" @click="changeView()">Checkout</v-btn>
        </v-col> 
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      digits: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "00"],
    };
  },
  methods: {
    keyboardValue(d) {
      this.$emit("keyboard", d);
    },
    clearCart() {
      this.$emit("clearCart");
    },
    toggleTeam() {
      this.$emit("toggleTeam");
    },
    changeView() {
      this.$emit("changeView");
    },
    deleteFromCart() {
      this.$emit("deleteFromCart");
    },
    increaseProductAmount() {
      this.$emit("increaseProductAmount");
    },
    decreaseProductAmount() {
      this.$emit("decreaseProductAmount");
    },
  },
};
</script>

<style>
</style>