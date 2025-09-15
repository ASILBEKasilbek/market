function toggleFavorite(productId) {
  let favorites = JSON.parse(localStorage.getItem('favorites')) || [];
  if (favorites.includes(productId)) {
    favorites = favorites.filter(id => id !== productId);
    alert('Sevimlilardan o‘chirildi');
  } else {
    favorites.push(productId);
    alert('Sevimlilarga qo‘shildi');
  }
  localStorage.setItem('favorites', JSON.stringify(favorites));
}