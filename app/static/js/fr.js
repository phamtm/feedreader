var call_async = function (url, requestType, requestData, callback) {
  $.ajax({
    crossDomain: 'true',
    dataType: 'json',
    headers: {
      'Authorization': 'Basic ' + btoa(AUTH_TOKEN + ': ')
    },
    async: true,
    data: requestData,
    type: requestType,
    url: url,
    success: function (json) {
      console.log(json);
      if (typeof(callback) === 'function') {
        callback(json);
      }
    },
    error: function (xhr, ajaxOptions, thrownError) {
      console.log(requestData);
      console.log(xhr);
      console.log('Error at :: ' + url);
      console.log('Error :: ' + thrownError);
    }
  });
};

var upview = function (article_id) {
  call_async('http://localhost:5000/api/v1.0/article/upview',
             'GET',
             {'article_id':article_id});
};


var upview = function (article_id) {
  call_async('http://localhost:5000/api/v1.0/article/upview',
             'GET',
             {'article_id':article_id});
};

var upvote = function (article_id) {
  call_async('http://localhost:5000/api/v1.0/article/upvote',
             'GET',
             {'article_id':article_id});
};

var downvote = function (article_id) {
  call_async('http://localhost:5000/api/v1.0/article/downvote',
             'GET',
             {'article_id':article_id});
};

var remove_vote = function (article_id) {
  call_async('http://localhost:5000/api/v1.0/article/remove_vote',
             'GET',
             {'article_id':article_id});
};

var list_magazines = function () {
  call_async('http://localhost:5000/api/v1.0/magazine/list_magazines',
             'GET',
             {'article_id':article_id});
};

var add_article_to_magazine = function (article_id, magazine_id) {
  call_async('http://localhost:5000/api/v1.0/magazine/add_article',
             'GET',
             {'article_id':article_id, 'magazine_id':magazine_id});
};


$('.article-upview').click(function() {
  var article_id = $(this).data('id');
  upview(article_id);
  return false;
});

$('.article-upvote').click(function() {
  var article_id = $(this).data('id');
  console.log(article_id);
  upvote(article_id);
  return false;
});

$('.article-downvote').click(function() {
  var article_id = $(this).data('id');
  downvote(article_id);
});

$('.article-remove-vote').click(function() {
  var article_id = $(this).data('id');
  remove_vote(article_id);
});
