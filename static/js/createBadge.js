function createBadge(text, colorClass) {
    var badge = document.createElement('span');
    badge.classList.add('badge');
    badge.classList.add(colorClass);
    badge.textContent = text;

    var removeButton = document.createElement('span');
    removeButton.classList.add('remove-badge');
    removeButton.textContent = 'x';
    removeButton.addEventListener('click', function () {
        badge.parentNode.removeChild(badge);
    });

    badge.appendChild(removeButton);
    return badge;
}

function addBadge(container, text, colorClass) {
    var badgeContainer = document.getElementById(container);
    var badge = createBadge(text, colorClass);
    badgeContainer.appendChild(badge);
}

document.getElementById('selectOptions1').addEventListener('change', function () {
    var selectedOption = this.options[this.selectedIndex];
    if (selectedOption.value) {
        addBadge('badgeContainer', selectedOption.textContent, 'badge');
    }
});

document.getElementById('selectOptions2').addEventListener('change', function () {
    var selectedOption = this.options[this.selectedIndex];
    if (selectedOption.value) {
        addBadge('badgeContainer', selectedOption.textContent, 'badge-green');
    }
});

// Enviar
document.getElementById('enviar').addEventListener('click', function () {
    var badges1 = document.querySelectorAll('.badge[data-type="1"]');
    var values1 = [];
    badges1.forEach(function (badge) {
        values1.push(badge.textContent);
    });
    var concatenatedValues1 = values1.join(',');
    document.getElementById('badgeValues1').value = concatenatedValues1;

    var badges2 = document.querySelectorAll('.badge[data-type="2"]');
    var values2 = [];
    badges2.forEach(function (badge) {
        values2.push(badge.textContent);
    });
    var concatenatedValues2 = values2.join(',');
    document.getElementById('badgeValues2').value = concatenatedValues2;

    // Agora o formulário será enviado com os valores das badges separados
});