package server

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

func TestItems(t *testing.T) {
	h := New()
	tests := []struct {
		method, path, body string
		want               int
	}{
		{"GET", "/healthz", "", http.StatusOK},
		{"POST", "/api/v1/items", `{"id":1,"name":"a"}`, http.StatusCreated},
		{"POST", "/api/v1/items", `{"id":1,"name":"a"}`, http.StatusConflict},
		{"POST", "/api/v1/items", `not json`, http.StatusBadRequest},
		{"GET", "/api/v1/items/1", "", http.StatusOK},
		{"GET", "/api/v1/items/2", "", http.StatusNotFound},
		{"GET", "/api/v1/items/x", "", http.StatusBadRequest},
	}
	for _, tt := range tests {
		rec := httptest.NewRecorder()
		h.ServeHTTP(rec, httptest.NewRequest(tt.method, tt.path, strings.NewReader(tt.body)))
		if rec.Code != tt.want {
			t.Errorf("%s %s = %d, want %d", tt.method, tt.path, rec.Code, tt.want)
		}
	}
}
