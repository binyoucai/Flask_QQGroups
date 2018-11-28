    var _auth = false;

    function changeStatus(status) {
        switch (status) {
            case 0:
                $('#tips').text('手机 QQ 扫描二维码');
                break;
            case 1:
                $('#tips').text('二维码认证中...');
                break;
            case 2:
                $('#login_success').css('display', 'inline-block');
                $('#tips').text('登录成功，点击可刷新');
                _auth = true;
                break;
            case 3:
                $('#qr_invalid').css('display', 'inline-block');
                $('#tips').text('二维码失效，请点击刷新');
                _auth = false;
                break;
            default:
                console.log(status);
        }
    }

    function qrLoginQuery() {
        function trigger() {
            var url = '/login/?t=' + (new Date().getTime());
            $.ajax({
                url: url,
                cache: false,
                dataType: "json",
                success: function(obj) {
                    var status = JSON.parse(JSON.stringify(obj)).status;
                    changeStatus(status);
                    if ([2, 3].includes(status)) {
                        clearInterval(window.queryTimmer);
                    }
                }
            });
        }
        window.queryTimmer = setInterval(trigger, 2000);
    }

    function qrRefresh() {
        _auth = false;
        clearInterval(window.queryTimmer);
        $('#qrcode').attr('src', '');
        var src = '/getqrcode?r=' + Math.random();
        $('#qrcode').attr('src', src);
        $('#login_success').css('display', 'none');
        $('#qr_invalid').css('display', 'none');
        $('#tips').text('手机 QQ 扫描二维码');
        qrLoginQuery();
    }

    (function() {
        qrRefresh();
        $("#the_form").submit(function(e) {
            e.preventDefault();
            if (!_auth) {
                alert('请先扫码授权登录');
            }
            else {
                $(".kwbox p").css("background", "url('../../img/ajax-loader.gif') center center no-repeat");
                $("input[type=submit]").prop("disabled", true);
                $.ajax({
                    type: "POST",
                    url: "/index/",
                    data: $(this).serializeArray(),
                    success: function(data) {

                        $(".kwbox p").css("background", "");
                        $("input[type=submit]").prop("disabled", false);
                        var path = '/download?token=' + data['token'];
                        window.open(path, "_blank");
                    },
                    error: function() {
                        $(".kwbox p").css("background", "");
                        $("input[type=submit]").prop("disabled", false);
                    }
                });
            }
            return false;
        });
    })();