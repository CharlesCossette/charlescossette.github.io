function resizeGridItem(item) {
    const grid = document.getElementsByClassName('gallery')[0];
    const rowHeight = parseInt(window.getComputedStyle(grid).getPropertyValue('grid-auto-rows'));
    const rowGap = parseInt(window.getComputedStyle(grid).getPropertyValue('gap'));
    const img = item.querySelector('img');
    const imgHeight = img.getBoundingClientRect().height;
    const rowSpan = Math.ceil((imgHeight + rowGap) / (rowHeight + rowGap));
    item.style.setProperty('--row-span', rowSpan);
}

function resizeAllGridItems() {
    const allItems = document.getElementsByClassName('gallery-item');
    for (let i = 0; i < allItems.length; i++) {
        resizeGridItem(allItems[i]);
    }
}

window.onload = resizeAllGridItems;
window.addEventListener('resize', resizeAllGridItems);

const allImages = document.querySelectorAll('.gallery-item img');
allImages.forEach(function(img) {
    img.addEventListener('load', function() {
        const item = img.parentElement;
        resizeGridItem(item);
    });
});