<template>
  <v-card color="surface" class="cart-card d-flex flex-column">
    <v-card-title class="d-flex align-center justify-space-between pa-3">
      <div class="d-flex align-center">
        <v-icon class="mr-2" size="20">mdi-cart</v-icon>
        <span class="text-h6 font-weight-bold">Cart</span>
        <v-chip
          v-if="isteam"
          color="success"
          size="small"
          class="ml-2"
          variant="flat"
        >
          <v-icon start size="14">mdi-account-group</v-icon>
          Team
        </v-chip>
      </div>
      <v-chip
        v-if="productsinCart.length > 0"
        size="small"
        color="primary"
        variant="tonal"
      >
        {{ productsinCart.length }} {{ productsinCart.length === 1 ? 'item' : 'items' }}
      </v-chip>
    </v-card-title>

    <v-divider />

    <v-card-text class="flex-grow-1 overflow-y-auto pa-0" style="max-height: 250px;">
      <div v-if="productsinCart.length === 0" class="d-flex flex-column align-center justify-center pa-8 text-medium-emphasis">
        <v-icon size="48" class="mb-2" color="surface-variant">mdi-cart-outline</v-icon>
        <div class="text-body-2">Cart is empty</div>
        <div class="text-caption">Tap a product to add it</div>
      </div>

      <v-list v-else density="compact" class="pa-1" bg-color="transparent">
        <v-list-item
          v-for="(product, index) in productsinCart"
          :key="index"
          :value="index"
          @click="selectProduct(index)"
          :active="selectedProductIndex === index"
          active-color="primary"
          rounded="lg"
          class="mx-1 my-1 cart-item"
        >
          <template v-slot:prepend>
            <v-avatar
              :color="selectedProductIndex === index ? 'primary' : 'surface-variant'"
              size="32"
              class="text-caption font-weight-bold"
            >
              {{ product.amount }}x
            </v-avatar>
          </template>

          <v-list-item-title class="text-body-2 font-weight-medium">
            {{ product.name }}
          </v-list-item-title>
          <v-list-item-subtitle class="text-caption">
            {{ formatPrice(product.price) }} each
          </v-list-item-subtitle>

          <template v-slot:append>
            <span class="text-body-2 font-weight-bold">
              {{ formatPrice(product.price * product.amount) }}
            </span>
          </template>
        </v-list-item>
      </v-list>
    </v-card-text>

    <v-divider />

    <v-card-actions class="pa-3">
      <v-row dense align="center">
        <v-col v-if="amountKeyboard" cols="auto">
          <v-chip size="small" color="info" variant="tonal">
            <v-icon start size="14">mdi-keyboard</v-icon>
            Qty: {{ amountKeyboard }}
          </v-chip>
        </v-col>
        <v-spacer />
        <v-col cols="auto" class="text-right">
          <div class="text-caption text-medium-emphasis">Total</div>
          <div class="text-h5 font-weight-bold" :class="calculatedtotal > 0 ? 'text-primary' : ''">
            {{ formatPrice(calculatedtotal) }}
          </div>
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
    formatPrice(price) {
      price = parseFloat(price);
      if (Number.isNaN(price)) return "0.00€";
      return `${price.toFixed(2)}€`;
    },
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
      type: [String, Number],
      default: "",
    },
    productsinCart: {
      type: Array,
      default: () => [],
    },
    isteam: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

<style scoped>
.cart-card {
  border: 1px solid rgba(255, 255, 255, 0.06);
}
.cart-item {
  transition: all 0.1s ease;
}
</style>
