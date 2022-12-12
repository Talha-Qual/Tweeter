follow_btn = document.querySelector("#follow-btn");
follow_btn.addEventListener("click", (e) => {
  user = follow_btn.getAttribute("data-user");
  user_action = follow_btn.textContent.trim();
  form = new FormData();
  form.append("user", user);
  form.append("user_action", user_action);
  fetch("/follow/", {
    method: "POST",
    body: form,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data)
      follow_btn.textContent = data.user_action;
      document.querySelector(
        "#follower"
      ).textContent = `Followers ${data.follower_count}`;
    });
});