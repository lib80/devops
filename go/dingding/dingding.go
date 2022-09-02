package dingding

import (
    "bytes"
    "crypto/hmac"
    "crypto/sha256"
    "encoding/base64"
    "encoding/json"
    "fmt"
    "net/http"
    "net/url"
    "time"
)

const (
    accessToken = "xxx"
    secret = "xxx"
)

func GetDynamicWebhook() string {
    timestamp := time.Now().UnixNano() / 1e6
    stringToSign := fmt.Sprintf("%v\n%v", timestamp, secret)
    h := hmac.New(sha256.New, []byte(secret))
    h.Write([]byte(stringToSign))
    base64Code := base64.StdEncoding.EncodeToString(h.Sum(nil))
    sign := url.QueryEscape(base64Code)
    return fmt.Sprintf("https://oapi.dingtalk.com/robot/send?access_token=%v&timestamp=%v&sign=%v", accessToken, timestamp, sign)
}

func SendNotify(msg string) {
    webhook := GetDynamicWebhook()
    fmt.Println(webhook)
    at := map[string]interface{}{
        "atMobiles": []string{"133xxxxxxxx"},
        "isAtAll": false,
    }
    text := map[string]string{
        "content": msg,
    }
    data := map[string]interface{}{
        "at": at,
        "text": text,
        "msgtype": "text",
    }
    bs, _ := json.Marshal(data)
    resp, err := http.Post(webhook, "application/json", bytes.NewBuffer(bs))
    if err != nil {
        fmt.Println(err)
        return
    }
    defer resp.Body.Close()
    //body, _ := ioutil.ReadAll(resp.Body)
    //fmt.Println(string(body))
}
