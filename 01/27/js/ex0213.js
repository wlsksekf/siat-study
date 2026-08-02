function updateAll() {
        let totalCount = 0;
        let totalPrice = 0;
        const prices = document.querySelectorAll(".price");

        for (let i = 0; i < 3; i++) {
            const inputEl = document.getElementById(`book${i + 1}`);
            let inputValue = inputEl.value.replace(/\s+/g, ""); 
            
            if (isNaN(inputValue) || inputValue === "") {
                inputValue = 0;
            } else {
                inputValue = parseInt(inputValue);
            }
            
            inputEl.value = inputValue;

            const unitPrice = Number(prices[i].textContent.replace(/,|원/g, ""));
            const subTotal = unitPrice * inputValue;

            document.getElementById(`book${i + 1}Total`).value = subTotal.toLocaleString();
            
            totalCount += inputValue;
            totalPrice += subTotal;
        }

        document.getElementById("totalNumber").value = totalCount.toLocaleString();
        document.getElementById("totalPrice").value = totalPrice.toLocaleString();
    }

    document.querySelector('form').addEventListener('input', updateAll);
    document.querySelector('input[type="reset"]').addEventListener('click', () => {
        setTimeout(updateAll, 0);
    });