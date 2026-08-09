<template>
  <div class="pay-panel">
    <v-card color="surface" class="mb-4 pa-5" style="border: 1px solid rgba(255,255,255,0.12);">
      <div class="text-center mb-4">
        <div class="text-caption text-uppercase" style="color: #aaa; letter-spacing: 2px;">Amount Due</div>
        <div class="text-h3 font-weight-bold text-primary mt-1">{{ formatPrice(total) }}</div>
      </div>

      <v-divider class="my-4" />

      <div class="text-subtitle-2 mb-3" style="color: #ccc;">Quick cash</div>
      <v-row dense class="mb-4">
        <v-col cols="3" v-for="amount in [5, 10, 20, 50]" :key="amount">
          <v-btn
            block
            size="large"
            :variant="selectedAmount === amount ? 'flat' : 'outlined'"
            :color="selectedAmount === amount ? 'secondary' : undefined"
            @click="selectCashAmount(amount)"
            class="cash-btn"
          >
            {{ amount }}€
          </v-btn>
        </v-col>
      </v-row>

      <div class="text-subtitle-2 mb-2" style="color: #ccc;">Or enter custom amount</div>
      <v-text-field
        v-model="customAmount"
        type="number"
        step="0.01"
        min="0"
        placeholder="e.g. 7.50"
        prepend-inner-icon="mdi-currency-eur"
        variant="outlined"
        density="comfortable"
        hide-details="auto"
        class="mb-4"
        @focus="selectedAmount = null"
      />

      <v-card
        v-if="changeVisible"
        :color="changeValue >= 0 ? '#1a3329' : '#331a1a'"
        class="pa-4 mb-4 text-center"
        flat
        style="border: 1px solid rgba(255,255,255,0.08);"
      >
        <div class="text-caption" style="color: #aaa;">Change to return</div>
        <div
          class="text-h4 font-weight-bold"
          :class="changeValue >= 0 ? 'text-success' : 'text-error'"
        >
          {{ formatPrice(changeValue) }}
        </div>
      </v-card>

      <v-alert
        v-if="validationError"
        type="error"
        variant="tonal"
        density="compact"
        class="mb-3"
        closable
        @click:close="validationError = ''"
      >
        {{ validationError }}
      </v-alert>
    </v-card>

    <v-row dense>
      <v-col cols="6">
        <v-btn
          block
          size="x-large"
          variant="outlined"
          @click="$emit('goBack')"
          class="back-btn"
        >
          <v-icon start>mdi-arrow-left</v-icon>
          Back
        </v-btn>
      </v-col>
      <v-col cols="6">
        <v-btn
          block
          size="x-large"
          color="primary"
          variant="flat"
          @click="confirmPayment"
          :disabled="!movieselected || total === 0"
        >
          <v-icon start>mdi-check-circle</v-icon>
          Confirm
        </v-btn>
      </v-col>
    </v-row>

    <v-alert
      v-if="!movieselected"
      type="warning"
      variant="tonal"
      density="compact"
      class="mt-3"
    >
      Please select a movie first
    </v-alert>

    <v-alert
      v-else-if="total === 0"
      type="info"
      variant="tonal"
      density="compact"
      class="mt-3"
    >
      Cart is empty — add items before paying
    </v-alert>
  </div>
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
      selectedAmount: null,
      customAmount: "",
      validationError: "",
    };
  },
  computed: {
    paidAmount() {
      if (this.selectedAmount !== null) return this.selectedAmount;
      if (this.customAmount !== "" && !isNaN(parseFloat(this.customAmount))) {
        return parseFloat(this.customAmount);
      }
      return null;
    },
    changeVisible() {
      return this.paidAmount !== null;
    },
    changeValue() {
      if (this.paidAmount !== null) {
        return this.paidAmount - this.total;
      }
      return 0;
    },
  },
  methods: {
    selectCashAmount(amount) {
      this.selectedAmount = this.selectedAmount === amount ? null : amount;
      this.customAmount = "";
      this.validationError = "";
    },
    confirmPayment() {
      if (!this.movieselected) return;
      if (this.total === 0) {
        this.validationError = "Cart is empty. Please add items first.";
        return;
      }
      if (this.paidAmount === null) {
        this.validationError = "Please enter the paid amount or select a cash option first.";
        return;
      }
      if (this.paidAmount < this.total) {
        this.validationError = `Insufficient payment. Customer needs to pay at least ${this.formatPrice(this.total)}.`;
        return;
      }
      this.validationError = "";
      this.$emit("checkout");
      this.selectedAmount = null;
      this.customAmount = "";
    },
    formatPrice(price) {
      price = parseFloat(price);
      if (Number.isNaN(price)) return "0.00€";
      return `${price.toFixed(2)}€`;
    },
  },
};
</script>

<style scoped>
.cash-btn {
  font-weight: 600;
  font-size: 1rem;
  text-transform: none;
  letter-spacing: 0;
  border-color: rgba(255, 255, 255, 0.2) !important;
  color: #EAEAEA !important;
}
.cash-btn:hover {
  border-color: rgba(78, 205, 196, 0.5) !important;
  background: rgba(255, 255, 255, 0.05);
}
.back-btn {
  border-color: rgba(255, 255, 255, 0.2) !important;
  color: #EAEAEA !important;
}
</style>
