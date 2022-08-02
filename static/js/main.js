function textOnHover(){

    const box = document.getElementById('tick');

    // 👇️ Change text color on mouseover
    box.addEventListener('mouseover', function handleMouseOver() {
    box.innerHTML = "Click here to buy this ticket";
    });

    // 👇️ Change text color back on mouseout
    box.addEventListener('mouseout', function handleMouseOut() {
    box.style.color = 'black';
    });
}