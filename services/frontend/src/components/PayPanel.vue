<template>
  <v-container fluid>
    <v-row>
      <v-col cols="6">
        <v-row>
          <v-col cols="3">
            <v-img src="@/assets/5.jpg" @click="handleButtonClick(5)"></v-img>
          </v-col>
          <v-col cols="3">
            <v-img src="@/assets/10.jpg" @click="handleButtonClick(10)"></v-img>
          </v-col>
          <v-col cols="3">
            <v-img src="@/assets/20.jpg" @click="handleButtonClick(20)"></v-img>
          </v-col>
          <v-col cols="3">
            <v-img src="@/assets/50.jpg" @click="handleButtonClick(50)"></v-img>
          </v-col>
        </v-row>
      </v-col>
      <v-col cols="6" class="d-flex align-center justify-center">
        <v-card
          @click="handleButtonClick(0)"
          color="primary"
          class="mx-auto"
          height="200"
          rounded="xl"
          width="200"
        >
          <div
            class="text-h6 text-md-h4 fill-height d-flex align-center justify-center"
          >
            Pay
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
  <v-dialog v-model="dialog" max-width="600">
    <v-card>
      <v-card-title class="text-h5">Payment Details</v-card-title>
      <v-card-text>
        <div v-if="movieselected">
          <div class="text-h6">Total: {{ formatPrice(total) }}</div>
          <div class="text-h6">Change: {{ formatPrice(calculateChange(changeamount)) }}</div>
        </div>
        <div v-else>
            <v-alert text="Please select a movie first" type="error"></v-alert>
        </div>
      </v-card-text>
      <v-card-actions v-if="movieselected">
        <v-btn color="primary" @click="closeDialog">Book</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {
    total: {
      type: Number,
      default: 0,
    },
    amountKeyboard: {
      type: String,
      default: "",
    },
    movieselected: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      dialog: false,
      changeamount: 0,
    };
  },
  methods: {
    handleButtonClick(amount) {
      this.dialog = true;
      this.changeamount = amount;
    },
    closeDialog() {
      this.dialog = false;
      this.changeamount = 0;
      this.$emit("checkout");
    },
    calculateChange(given) {
      if (given !== 0) {
        return given - this.total;
      } else if (given === 0 && this.amountKeyboard === "") {
        return 0;
      } else {
        return parseFloat(this.amountKeyboard) - this.total;
      }
    },
    formatPrice(price) {
      price = parseFloat(price);
      if (Number.isNaN(price)) {
        return "0.00€";
      }
      const priceString = price.toString();
      if (priceString.includes(".") && priceString.split(".")[1].length === 2) {
        return `${price.toFixed(2)}€`;
      } else {
        return `${price.toFixed(2).replace(/\.0{2}$/, "")}€`;
      }
    },
  },
};
</script>

<style>
</style>
