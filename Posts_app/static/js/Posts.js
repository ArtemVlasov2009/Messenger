let modal = document.querySelector(".modal-win"); 
let modalAll = document.querySelector(".modal") 
let openModal = document.getElementById("open-modal"); 
let closeModal = document.querySelector(".close"); 
 
openModal.onclick = function() { 
  modal.style.display = "block"; 
  modalAll.style.display = "block"; 
} 
 
closeModal.onclick = function() { 
  modal.style.display = "none"; 
  modalAll.style.display = "none"; 
} 
document.addEventListener('DOMContentLoaded', function() { 
    let dotsButtons = document.querySelectorAll('.dots-button'); 
     
    dotsButtons.forEach(button => { 
        button.addEventListener('click', function(e) { 
            e.stopPropagation(); 
            let menu = this.nextElementSibling; 
             
            document.querySelectorAll('.dropdown-menu.show').forEach(m => { 
                if (m !== menu) m.classList.remove('show'); 
            }); 
             
            menu.classList.toggle('show'); 
        }); 
    }); 
     
    document.addEventListener('click', function() { 
        document.querySelectorAll('.dropdown-menu.show').forEach(menu => { 
            menu.classList.remove('show'); 
        }); 
    }); 
     
    document.querySelectorAll('.dropdown-menu').forEach(menu => { 
        menu.addEventListener('click', function(e) { 
            e.stopPropagation(); 
        }); 
    }); 
}); 
document.addEventListener('DOMContentLoaded', function() { 
     
    document.querySelectorAll('.delete-btn').forEach(button => { 
        button.addEventListener('click', function(e) { 
            e.preventDefault(); 
             
 
        }); 
    }); 
     
});