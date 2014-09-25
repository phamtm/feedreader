var call_async = function (url, requestType, requestData, callback) {
    $.ajax({
      async: true,
      crossDomain: 'true',
      data: requestData,
      dataType: 'json',
      type: requestType,
      url: url,
      success: function (json) {
          // callback(json);
        if (typeof(callback) === 'function') {
          callback(json);
        }
      },
      error: function (xhr, ajaxOptions, thrownError) {
        console.log(requestData);
        console.log('Error at :: ' + url);
        console.log('Error :: ' + thrownError);
      }
    });
  };