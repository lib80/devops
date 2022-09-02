        function resolveData(data) {
            var arr = []
            for (k in data) {
                arr.push(k + "=" + data[k])
            }
            return arr.join('&')
        }
        
        function customAjax(option) {
            var xhr = new XMLHttpRequest()

            if (option.method.toUpperCase() === 'GET') {
                xhr.open('GET', option.url + '?' + resolveData(option.data))
                xhr.send()
            } else if (option.method.toUpperCase() === 'POST') {
                xhr.open('POST', option.url)
                xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')
                xhr.send(resolveData(option.data))
            }

            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    var res = JSON.parse(xhr.responseText)
                    option.success(res)
                }
            }
        }
