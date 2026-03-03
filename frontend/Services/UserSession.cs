using Microsoft.JSInterop;
using System.Net.Http.Json;

namespace frontend.Services
{
  public class UserSession
  {
    private readonly HttpClient _http;
    private readonly IJSRuntime _js;

    public int? UserId { get; private set; }
    public string? Username { get; private set; }
    public bool IsLoggedIn => UserId.HasValue;

    public event Action? OnChange;

    public UserSession(HttpClient http, IJSRuntime js)
    {
      _http = http;
      _js = js;
    }

    public async Task InitializeAsync()
    {
      var storedUser = await _js.InvokeAsync<string>("localStorage.getItem", "toolbox_user");
      if (!string.IsNullOrEmpty(storedUser))
      {
        var parts = storedUser.Split('|');
        if (parts.Length == 2 && int.TryParse(parts[0], out int id))
        {
          UserId = id;
          Username = parts[1];
          NotifyStateChanged();
        }
      }
    }

    public async Task<bool> LoginAsync(string username, string password)
    {
      var response = await _http.PostAsync($"https://api-creativedevtool.rsanjur.com/auth/login?username={username}&password={password}", null);
      if (response.IsSuccessStatusCode)
      {
        var user = await response.Content.ReadFromJsonAsync<UserDto>();
        if (user != null)
        {
          UserId = user.Id;
          Username = user.Username;
          await _js.InvokeVoidAsync("localStorage.setItem", "toolbox_user", $"{user.Id}|{user.Username}");
          NotifyStateChanged();
          return true;
        }
      }
      return false;
    }

    public async Task<string?> RegisterAsync(string username, string password)
    {
      var response = await _http.PostAsync($"https://api-creativedevtool.rsanjur.com/auth/register?username={username}&password={password}", null);
      if (response.IsSuccessStatusCode)
      {
        return null; // Success
      }
      else
      {
        var error = await response.Content.ReadAsStringAsync();
        return error ?? "Error al registrarse";
      }
    }

    public async Task LogoutAsync()
    {
      UserId = null;
      Username = null;
      await _js.InvokeVoidAsync("localStorage.removeItem", "toolbox_user");
      NotifyStateChanged();
    }

    private void NotifyStateChanged() => OnChange?.Invoke();

    private class UserDto
    {
      public int Id { get; set; }
      public string Username { get; set; } = "";
    }
  }
}
