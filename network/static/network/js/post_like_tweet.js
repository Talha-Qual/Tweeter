document.addEventListener('DOMContentLoaded', ()=> {
  document.querySelector('#tweet-form').onsubmit = ()=> {
    form = document.querySelector('#tweet-form');
    const formData = new FormData(form);
    fetch(form.action, {
      method: "POST",
      body: formData
    })
    .then(response => response.json())
    .then (data => {
      console.log(data)
      create_tweet_box(data);
    })
    document.querySelector('#tweet-text').value = '';
    return false;
}})


function make_div(className) {
div = document.createElement("div");
div.setAttribute("class", className);
return div;
}

function make_span(className) {
span = document.createElement("span");
span.setAttribute("class", className);
return span;
}

function create_tweet_box(data) {
  const div1 = make_div('post');
  const div2 = make_div('post__avatar');
  const img1 = document.createElement('img');
  img1.setAttribute('src', "https://i.pinimg.com/originals/a6/58/32/a65832155622ac173337874f02b218fb.png");
  // profile image here TODO
  const div3 = make_div('post__body');
  const div4 = make_div('post__header');
  const div5 = make_div('post__headerText');
  const h3 = document.createElement("h3"); // where users name will go
  h3.innerHTML = `${data["tweeter"]}`;
  const span1 = make_span('post__headerSpecial');
  const span2 = make_span('material-icons post__badge');
  span2.innerHTML = 'verified';
  const div7 = make_div('post__headerDescription');
  const p = document.createElement('p');
  p.innerHTML = `${data["tweet"]}`;
  // image here if user posts one
  const img2 = document.createElement('img');
  img2.setAttribute('src', "https://www.focus2move.com/wp-content/uploads/2020/01/Tesla-Roadster-2020-1024-03.jpg");

  const div8 = make_div('post__footer');
  const span3 = make_span('material-icons');
  span3.innerHTML = 'repeat';

  // like stuff
  id_val = `${data["tweet_id"]}`
  const img3 = document.createElement("img");
  img3.setAttribute("class", "like-selected");
  img3.setAttribute("data-id", id_val);
  img3.setAttribute("id", `tweet-like-${id_val}`);
  img3.setAttribute("data-liked", 'no');
  img3.setAttribute("src", "/static/network/images/heart_unlike.png");
  like_tweet(img3)
  const span6 = document.createElement("span");
  span6.setAttribute("id", `like-count-${id_val}`);
  span6.textContent = "0";

  // publish and appending stuff
  const span5 = make_span('material-icons');
  span5.innerHTML = 'publish';

  div7.appendChild(p);
  span1.appendChild(span2);
  h3.appendChild(span1);
  div5.appendChild(h3);
  div5.appendChild(div7);
  div4.appendChild(div5);
  div8.appendChild(span3);
  div8.appendChild(img3);
  div8.appendChild(span6);
  div8.appendChild(span5);
  div3.appendChild(div4);
  div3.appendChild(img2);
  div3.appendChild(div8);
  div2.appendChild(img1);
  div1.appendChild(div2);
  div1.appendChild(div3);
  document.querySelector('#over-post').prepend(div1);
}