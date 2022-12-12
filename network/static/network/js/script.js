
like = document.querySelectorAll(".like-selected");
like.forEach((element) => {
  like_tweet(element);
});

// Function to handle likes. Gets called in layout.html
function like_tweet(element) {
  element.addEventListener("click", () => {
    id = element.getAttribute("data-id");
    console.log(id)
    liked = element.getAttribute("data-liked");
    icon = document.querySelector(`#tweet-like-${id}`);
    count = document.querySelector(`#like-count-${id}`);
    form = new FormData();
    form.append("id", id);
    form.append("liked", liked);
    fetch("/like/", {
      method: "POST",
      body: form
    })
    .then(response => response.json())
    .then (data => {
      if (data.status == 200 ){
        if (data.liked === 'yes') {
          icon.src = '/static/network/images/heart_like.png';
          element.setAttribute('data-liked', 'yes')
        } else {
          icon.src = '/static/network/images/heart_unlike.png';
          element.setAttribute('data-liked', 'no')
        }
        console.log(data.likes)
        console.log(id)
        count.innerHTML = data.likes;
      }
    });
  });
}