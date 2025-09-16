using System.Collections;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class IntroTypewriter : MonoBehaviour
{
    public TextMeshProUGUI introTextUI;
    [TextArea(3, 20)]
    public string[] textSegments; // Metin par�alar�
    public float typingSpeed = 0.05f;
    public CanvasGroup canvasGroup; // Fade i�in
    public float fadeDuration = 0.5f;
    public Button skipButton;       // "Ge�" butonu

    bool isTyping = false;
    int currentSegment = 0;

    void Start()
    {
        if (introTextUI == null) Debug.LogError("IntroTextUI atanmam��! Inspector'dan s�r�kle.");
        if (skipButton != null) skipButton.gameObject.SetActive(false);
        StartCoroutine(PlayIntro());
    }

    IEnumerator PlayIntro()
    {
        // Fade-in
        if (canvasGroup != null)
        {
            canvasGroup.alpha = 0f;
            float t = 0f;
            while (t < fadeDuration)
            {
                t += Time.deltaTime;
                canvasGroup.alpha = Mathf.Clamp01(t / fadeDuration);
                yield return null;
            }
            canvasGroup.alpha = 1f;
        }

        // Metinleri s�rayla g�ster
        for (currentSegment = 0; currentSegment < textSegments.Length; currentSegment++)
        {
            yield return StartCoroutine(TypeText(textSegments[currentSegment]));

            // "Ge�" butonunu aktif et
            if (skipButton != null)
            {
                skipButton.gameObject.SetActive(true);
                bool clicked = false;
                skipButton.onClick.RemoveAllListeners();
                skipButton.onClick.AddListener(() => clicked = true);

                // Buton t�klan�ncaya kadar bekle
                while (!clicked)
                    yield return null;

                skipButton.gameObject.SetActive(false);
            }

            // Bir sonraki metin gelmeden �nce eski metni kaybolacak
            yield return StartCoroutine(FadeOutText());
        }
        // Son segmentten sonra paneli kapat
        if (canvasGroup != null)
        {
            float t = 0f;
            float startAlpha = canvasGroup.alpha;
            while (t < fadeDuration)
            {
                t += Time.deltaTime;
                canvasGroup.alpha = Mathf.Lerp(startAlpha, 0f, t / fadeDuration);
                yield return null;
            }
        }

    }

    IEnumerator TypeText(string segment)
    {
        isTyping = true;
        introTextUI.text = "";

        for (int i = 0; i < segment.Length; i++)
        {
            introTextUI.text += segment[i];

            float timer = 0f;
            while (timer < typingSpeed)
            {
                if (Input.GetMouseButtonDown(0) || Input.GetKeyDown(KeyCode.Space))
                {
                    introTextUI.text = segment;
                    isTyping = false;
                    yield break;
                }
                timer += Time.deltaTime;
                yield return null;
            }

        }

        isTyping = false;
    }

    IEnumerator FadeOutText()
    {
        if (canvasGroup == null)
        {
            introTextUI.text = "";
            yield break;
        }

        float startAlpha = canvasGroup.alpha;
        float t = 0f;
        while (t < fadeDuration)
        {
            t += Time.deltaTime;
            canvasGroup.alpha = Mathf.Lerp(startAlpha, 0f, t / fadeDuration);
            yield return null;
        }
        canvasGroup.alpha = 1f; // sonraki metin i�in tekrar g�r�n�r
        introTextUI.text = "";
    }
}
