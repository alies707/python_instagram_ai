import os
import requests


class InstagramAPIError(Exception):
    pass


class InstagramClient:
    def __init__(self, access_token: str, api_version: str = "v25.0"):
        if not access_token:
            raise InstagramAPIError("INSTAGRAM_ACCESS_TOKEN تنظیم نشده است.")
        self.access_token = access_token
        self.base_url = f"https://graph.facebook.com/{api_version}"
        self.timeout = 20

    def _get(self, path: str, params: dict | None = None):
        params = params or {}
        params["access_token"] = self.access_token
        try:
            response = requests.get(
                f"{self.base_url}/{path.lstrip('/')}",
                params=params,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise InstagramAPIError(f"خطا در ارتباط با Meta API: {exc}") from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise InstagramAPIError("پاسخ نامعتبر از Meta API دریافت شد.") from exc

        if not response.ok or "error" in payload:
            error = payload.get("error", {})
            message = error.get("message", response.text)
            raise InstagramAPIError(f"خطای Instagram API: {message}")
        return payload

    def get_account(self):
        account_id = os.getenv("INSTAGRAM_ACCOUNT_ID", "")
        if not account_id:
            raise InstagramAPIError("INSTAGRAM_ACCOUNT_ID تنظیم نشده است.")
        fields = "id,username,name,biography,website,followers_count,follows_count,media_count,profile_picture_url"
        return self._get(account_id, {"fields": fields})

    def get_media(self, limit: int = 12):
        account_id = os.getenv("INSTAGRAM_ACCOUNT_ID", "")
        fields = "id,caption,media_type,media_url,thumbnail_url,permalink,timestamp,like_count,comments_count"
        payload = self._get(f"{account_id}/media", {"fields": fields, "limit": limit})
        return payload.get("data", [])

    def get_account_insights(self):
        account_id = os.getenv("INSTAGRAM_ACCOUNT_ID", "")
        metrics = "reach,accounts_engaged,profile_views"
        try:
            payload = self._get(
                f"{account_id}/insights",
                {"metric": metrics, "period": "day"},
            )
            return payload.get("data", [])
        except InstagramAPIError:
            return []

    def analyze_media(self, media_id: str):
        if not media_id:
            raise InstagramAPIError("شناسه پست ارسال نشده است.")
        fields = "id,caption,media_type,permalink,timestamp,like_count,comments_count"
        media = self._get(media_id, {"fields": fields})
        likes = int(media.get("like_count", 0) or 0)
        comments = int(media.get("comments_count", 0) or 0)
        followers = int(self.get_account().get("followers_count", 0) or 0)
        engagement_rate = round(((likes + comments) / followers * 100), 2) if followers else 0
        caption = media.get("caption", "") or ""
        return {
            "media": media,
            "likes": likes,
            "comments": comments,
            "followers": followers,
            "engagement_rate": engagement_rate,
            "caption_length": len(caption),
            "recommendations": self._recommend(engagement_rate, caption, comments),
        }

    @staticmethod
    def _recommend(rate: float, caption: str, comments: int):
        recommendations = []
        if rate < 1:
            recommendations.append("نرخ تعامل پایین است؛ هوک ابتدای محتوا و زمان انتشار را آزمایش کنید.")
        elif rate < 3:
            recommendations.append("عملکرد متوسط است؛ CTA واضح‌تر و محتوای تعاملی‌تر می‌تواند مفید باشد.")
        else:
            recommendations.append("عملکرد تعامل خوب است؛ ساختار این محتوا را برای پست‌های آینده تکرار کنید.")
        if len(caption) < 80:
            recommendations.append("کپشن کوتاه است؛ برای روایت، ارزش افزوده یا CTA فضای بیشتری در نظر بگیرید.")
        if comments == 0:
            recommendations.append("سوالی مشخص در انتهای کپشن اضافه کنید تا گفتگو شکل بگیرد.")
        return recommendations
