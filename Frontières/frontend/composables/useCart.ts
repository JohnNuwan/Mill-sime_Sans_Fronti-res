export interface CartItem {
  id: string
  barrel_id: string
  name: string
  origin_country: string
  volume_liters: number
  price: number
  quantity: number
  image_url?: string
  wood_type?: string
  previous_content?: string
}

export interface CartSummary {
  subtotal: number
  shipping: number
  tax: number
  total: number
  itemCount: number
}

export const useCart = () => {
  // État réactif du panier
  const items = useState<CartItem[]>('cart_items', () => [])
  const isOpen = useState<boolean>('cart_is_open', () => false)

  // Computed properties
  const cartItemCount = computed(() => 
    items.value.reduce((total, item) => total + item.quantity, 0)
  )

  const cartSubtotal = computed(() => 
    items.value.reduce((total, item) => total + (item.price * item.quantity), 0)
  )

  const cartSummary = computed((): CartSummary => {
    const subtotal = cartSubtotal.value
    const shipping = calculateShipping(subtotal)
    const tax = calculateTax(subtotal)
    const total = subtotal + shipping + tax

    return {
      subtotal,
      shipping,
      tax,
      total,
      itemCount: cartItemCount.value
    }
  })

  // Fonction pour ajouter un article au panier
  const addToCart = (barrel: Omit<CartItem, 'id' | 'quantity'>, quantity: number = 1): void => {
    const existingItemIndex = items.value.findIndex(item => item.barrel_id === barrel.barrel_id)

    if (existingItemIndex !== -1) {
      // Mettre à jour la quantité si l'article existe déjà
      items.value[existingItemIndex].quantity += quantity
    } else {
      // Ajouter un nouvel article
      const newItem: CartItem = {
        ...barrel,
        id: generateCartItemId(),
        quantity
      }
      items.value.push(newItem)
    }

    // Sauvegarder dans le localStorage
    saveCartToStorage()
    
    // Ouvrir le panier (optionnel)
    // isOpen.value = true
  }

  // Fonction pour mettre à jour la quantité d'un article
  const updateQuantity = (itemId: string, quantity: number): void => {
    if (quantity <= 0) {
      removeFromCart(itemId)
      return
    }

    const itemIndex = items.value.findIndex(item => item.id === itemId)
    if (itemIndex !== -1) {
      items.value[itemIndex].quantity = quantity
      saveCartToStorage()
    }
  }

  // Fonction pour supprimer un article du panier
  const removeFromCart = (itemId: string): void => {
    const itemIndex = items.value.findIndex(item => item.id === itemId)
    if (itemIndex !== -1) {
      items.value.splice(itemIndex, 1)
      saveCartToStorage()
    }
  }

  // Fonction pour vider le panier
  const clearCart = (): void => {
    items.value = []
    saveCartToStorage()
  }

  // Fonction pour calculer les frais de livraison
  const calculateShipping = (subtotal: number): number => {
    // Logique de calcul des frais de livraison
    // Peut être basée sur le poids, la destination, etc.
    if (subtotal >= 1000) {
      return 0 // Livraison gratuite au-dessus de 1000€
    } else if (subtotal >= 500) {
      return 50 // Frais réduits entre 500€ et 1000€
    } else {
      return 100 // Frais standard en dessous de 500€
    }
  }

  // Fonction pour calculer la TVA
  const calculateTax = (subtotal: number): number => {
    // TVA française standard (20%)
    return subtotal * 0.20
  }

  // Fonction pour générer un ID unique pour les articles du panier
  const generateCartItemId = (): string => {
    return `cart_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  // Fonction pour sauvegarder le panier dans le localStorage
  const saveCartToStorage = (): void => {
    if (process.client) {
      localStorage.setItem('cart_items', JSON.stringify(items.value))
    }
  }

  // Fonction pour charger le panier depuis le localStorage
  const loadCartFromStorage = (): void => {
    if (process.client) {
      const storedCart = localStorage.getItem('cart_items')
      if (storedCart) {
        try {
          items.value = JSON.parse(storedCart)
        } catch (error) {
          console.error('Erreur lors du chargement du panier:', error)
          items.value = []
        }
      }
    }
  }

  // Fonction pour ouvrir/fermer le panier
  const toggleCart = (): void => {
    isOpen.value = !isOpen.value
  }

  const openCart = (): void => {
    isOpen.value = true
  }

  const closeCart = (): void => {
    isOpen.value = false
  }

  // Fonction pour vérifier si un article est dans le panier
  const isInCart = (barrelId: string): boolean => {
    return items.value.some(item => item.barrel_id === barrelId)
  }

  // Fonction pour obtenir la quantité d'un article dans le panier
  const getItemQuantity = (barrelId: string): number => {
    const item = items.value.find(item => item.barrel_id === barrelId)
    return item ? item.quantity : 0
  }

  // Fonction pour appliquer un code promo
  const applyPromoCode = (code: string): { success: boolean; discount: number; message: string } => {
    // Logique pour appliquer les codes promo
    const promoCode = code.toUpperCase()
    
    if (promoCode === 'WELCOME10') {
      const discount = cartSubtotal.value * 0.10
      return {
        success: true,
        discount,
        message: 'Code promo appliqué : 10% de réduction'
      }
    } else if (promoCode === 'B2B20') {
      const discount = cartSubtotal.value * 0.20
      return {
        success: true,
        discount,
        message: 'Code promo appliqué : 20% de réduction B2B'
      }
    } else {
      return {
        success: false,
        discount: 0,
        message: 'Code promo invalide'
      }
    }
  }

  // Fonction pour procéder au checkout
  const proceedToCheckout = (): void => {
    if (items.value.length === 0) {
      // Afficher un message d'erreur
      return
    }

    // Rediriger vers la page de checkout
    navigateTo('/checkout')
    closeCart()
  }

  // Fonction pour sauvegarder le panier pour plus tard
  const saveForLater = (): void => {
    if (process.client) {
      localStorage.setItem('cart_saved', JSON.stringify(items.value))
      clearCart()
    }
  }

  // Fonction pour restaurer un panier sauvegardé
  const restoreSavedCart = (): void => {
    if (process.client) {
      const savedCart = localStorage.getItem('cart_saved')
      if (savedCart) {
        try {
          items.value = JSON.parse(savedCart)
          localStorage.removeItem('cart_saved')
        } catch (error) {
          console.error('Erreur lors de la restauration du panier:', error)
        }
      }
    }
  }

  // Fonction pour exporter le panier (CSV, PDF, etc.)
  const exportCart = (format: 'csv' | 'pdf' = 'csv'): void => {
    if (format === 'csv') {
      const csvContent = generateCSV()
      downloadCSV(csvContent, 'panier.csv')
    } else if (format === 'pdf') {
      // Logique pour générer un PDF
      console.log('Export PDF non implémenté')
    }
  }

  // Fonction pour générer le contenu CSV
  const generateCSV = (): string => {
    const headers = ['Nom', 'Pays d\'origine', 'Volume (L)', 'Prix unitaire', 'Quantité', 'Prix total']
    const rows = items.value.map(item => [
      item.name,
      item.origin_country,
      item.volume_liters.toString(),
      item.price.toString(),
      item.quantity.toString(),
      (item.price * item.quantity).toString()
    ])

    return [headers, ...rows]
      .map(row => row.map(cell => `"${cell}"`).join(','))
      .join('\n')
  }

  // Fonction pour télécharger un fichier CSV
  const downloadCSV = (content: string, filename: string): void => {
    if (process.client) {
      const blob = new Blob([content], { type: 'text/csv;charset=utf-8;' })
      const link = document.createElement('a')
      const url = URL.createObjectURL(blob)
      link.setAttribute('href', url)
      link.setAttribute('download', filename)
      link.style.visibility = 'hidden'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
  }

  // Initialiser le panier au chargement de l'application
  onMounted(() => {
    loadCartFromStorage()
  })

  // Sauvegarder automatiquement le panier lors des modifications
  watch(items, () => {
    saveCartToStorage()
  }, { deep: true })

  return {
    // État
    items: readonly(items),
    isOpen: readonly(isOpen),

    // Computed
    cartItemCount,
    cartSubtotal,
    cartSummary,

    // Actions
    addToCart,
    updateQuantity,
    removeFromCart,
    clearCart,
    toggleCart,
    openCart,
    closeCart,
    isInCart,
    getItemQuantity,
    applyPromoCode,
    proceedToCheckout,
    saveForLater,
    restoreSavedCart,
    exportCart
  }
}
