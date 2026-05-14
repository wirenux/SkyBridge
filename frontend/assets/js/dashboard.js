// Simple drag to reorder and collapse functionality
let draggedCard = null;
let touchStartX = 0;
let touchStartY = 0;

document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.card');
    
    cards.forEach(card => {
        const title = card.querySelector('.card-title');
        const chevron = card.querySelector('.card-chevron');
        
        if (title) {
            // Desktop drag
            title.draggable = true;
            
            title.addEventListener('dragstart', (e) => {
                draggedCard = card;
                card.classList.add('dragging');
                e.dataTransfer.effectAllowed = 'move';
            });
            
            title.addEventListener('dragend', () => {
                draggedCard = null;
                card.classList.remove('dragging');
            });

            // Mobile touch drag
            title.addEventListener('touchstart', (e) => {
                if (e.touches.length === 1) {
                    draggedCard = card;
                    touchStartX = e.touches[0].clientX;
                    touchStartY = e.touches[0].clientY;
                    card.classList.add('dragging');
                }
            }, { passive: true });

            title.addEventListener('touchmove', (e) => {
                if (draggedCard && e.touches.length === 1) {
                    e.preventDefault();
                    const dashboard = document.querySelector('.dashboard');
                    const cards = Array.from(dashboard.querySelectorAll('.card'));
                    
                    const touchY = e.touches[0].clientY;
                    
                    // Find card under touch point
                    cards.forEach(otherCard => {
                        if (otherCard !== draggedCard) {
                            const rect = otherCard.getBoundingClientRect();
                            if (touchY > rect.top && touchY < rect.bottom) {
                                if (touchY < rect.top + rect.height / 2) {
                                    otherCard.parentNode.insertBefore(draggedCard, otherCard);
                                } else {
                                    otherCard.parentNode.insertBefore(draggedCard, otherCard.nextSibling);
                                }
                            }
                        }
                    });
                }
            }, { passive: false });

            title.addEventListener('touchend', () => {
                draggedCard = null;
                card.classList.remove('dragging');
            }, { passive: true });

            // Collapse on click/tap
            title.addEventListener('click', (e) => {
                // Check if it's a quick tap (not a drag)
                const isTap = Math.abs(e.clientX - touchStartX) < 10 && 
                             Math.abs(e.clientY - touchStartY) < 10;
                
                if (e.target === chevron || e.target === title) {
                    e.preventDefault();
                    toggleCollapse(card);
                }
            });
        }

        // Desktop drag over
        card.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
            if (draggedCard && draggedCard !== card) {
                card.parentNode.insertBefore(draggedCard, card);
            }
        });
    });
});

function toggleCollapse(card) {
    const allContent = Array.from(card.children).slice(1);
    const chevron = card.querySelector('.card-chevron');
    
    if (card.classList.contains('collapsed')) {
        // Expand
        card.classList.remove('collapsed');
        allContent.forEach(el => el.style.display = '');
        if (chevron) chevron.textContent = '▾';
    } else {
        // Collapse
        card.classList.add('collapsed');
        allContent.forEach(el => el.style.display = 'none');
        if (chevron) chevron.textContent = '▸';
    }
}
