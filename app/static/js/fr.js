PNotify.prototype.options.delay ? (function() {
    PNotify.prototype.options.delay -= 7000;
}()) : (alert('Timer is already at zero.'))

var call_async = function (url, requestType, requestData, callback) {
  $.ajax({
    crossDomain: 'true',
    dataType: 'json',
    headers: {
      'Authorization': 'Basic ' + btoa(AUTH_TOKEN + ':')
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

var upview = function (article_id, callback) {
  call_async('http://localhost:5000/api/v1.0/article/upview',
             'GET',
             {'article_id':article_id},
             callback);
};


var upview = function (article_id, callback) {
  call_async('http://localhost:5000/api/v1.0/article/upview',
             'GET',
             {'article_id':article_id},
             callback);
};

var upvote = function (article_id, callback) {
  call_async('http://localhost:5000/api/v1.0/article/upvote',
             'GET',
             {'article_id':article_id},
             callback);
};

var downvote = function (article_id, callback) {
  call_async('http://localhost:5000/api/v1.0/article/downvote',
             'GET',
             {'article_id':article_id},
             callback);
};

var remove_vote = function (article_id, callback) {
  call_async('http://localhost:5000/api/v1.0/article/remove_vote',
             'GET',
             {'article_id':article_id},
             callback);
};

var list_magazines = function () {
  call_async('http://localhost:5000/api/v1.0/magazine/list_magazines',
             'GET',
             {'article_id':article_id});
};

var add_article_to_magazine = function (article_id, magazine_id, callback) {
  call_async('http://localhost:5000/api/v1.0/magazine/add_article',
             'GET',
             {'article_id':article_id, 'magazine_id':magazine_id},
             callback);
};


$('.article-upview').click(function() {
  var article_id = $(this).data('id');
  upview(article_id);
});

$('.article-upvote').click(function() {
  var article_id = $(this).data('id');
  upvote(article_id, function() {create_notice('Article upvoted')});
  return false;
});

$('.article-downvote').click(function() {
  var article_id = $(this).data('id');
  downvote(article_id, function() {create_notice('Article downvoted')});
  $(this).html('Downvoted')
  return false;
});

$('.article-remove-vote').click(function() {
  var article_id = $(this).data('id');
  remove_vote(article_id, function() {create_notice('Vote removed')});
  $(this).html('Vote removed')
  return false;
});

var create_notice = function (message) {
  notice = new PNotify({text:message, type:'info', opacity:.6});
  notice.get().click(function() {
    notice.remove();
  });
};
