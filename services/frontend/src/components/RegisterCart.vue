<template>
  <v-card>
    <v-card-title class="d-flex justify-space-between">
      <div>Cart</div>
      <v-chip color="success" v-if="isteam">Team</v-chip>
    </v-card-title>
    <v-divider></v-divider>
    <v-card-text class="overflow-y-auto" style="max-height: 250px;">
      <v-list>
        <v-list-item-group
          v-model="selectedProductIndex"
          active-class="primary"
        >
          <v-list-item
            v-for="(product, index) in productsinCart"
            :key="index"
            :value="index"
            class="w-100"
            @click="selectProduct(index)"
          >
            <v-list-item-content class="d-flex justify-space-between">
              <div>{{ product.amount }}x {{ product.name }}</div>
              <div>
                Price: {{ formatPrice(product.price) }} Total:
                {{ formatPrice(product.price * product.amount) }}
              </div>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-card-text>

    <v-divider></v-divider>
    <v-card-actions>
      <v-row>
        <v-col justify="start">
          <div class="text-h6">{{ this.amountKeyboard }}</div>
        </v-col>
        <v-col justify="end" class="text-right">
          <div class="text-h6">Total:</div>
        </v-col>
        <v-col justify="end" class="text-right">
          <div class="text-h6">{{ formatPrice(calculatedtotal) }}</div>
        </v-col>
      </v-row>
    </v-card-actions>
  </v-card>
</template>
  
<script>
export default {
  data() {
    return {
      total: 0,
      model: 1,
      selectedProductIndex: null,
      selectedProduct: null,
    };
  },
  computed: {
    calculatedtotal() {
      return this.productsinCart.reduce((total, product) => {
        return total + product.price * product.amount;
      }, 0);
    },
  },
  watch: {
    calculatedtotal(newTotal) {
      this.$emit("total", newTotal);
    },
  },
  methods: {
    // Format price to 2 decimal places
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
    // Select product in cart
    selectProduct(index) {
      if (this.selectedProductIndex !== index) {
        this.selectedProductIndex = index;
        this.selectedProduct = this.productsinCart[this.selectedProductIndex];
        this.$emit("selectProduct", this.selectedProduct);
      } else {
        this.selectedProductIndex = null;
        this.selectedProduct = null;
      }
    },
    clearSelection() {
      this.selectedProductIndex = null;
      this.selectedProduct = null;
    },
  },
  props: {
    amountKeyboard: {
      type: Number,
      default: 0,
    },
    productsinCart: {
      type: Array,
    },
    isteam: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

<style>
</style>
