;; ONLY AN EXAMPLE, change namespace
(ns cljs.auth
  (:require [reagent.core :as r]
            [cljs-http.client :as http]
            [cljs.core.async :refer [<! go]]))

;; ---- states ----
(defonce register-mode? (r/atom false))
(defonce username (r/atom ""))
(defonce password (r/atom ""))
(defonce confirm-password (r/atom ""))
(defonce email (r/atom ""))
(defonce phone (r/atom ""))
(defonce birthday (r/atom ""))
(defonce error-message (r/atom ""))

(defonce authenticated? (r/atom false))
(defonce loading? (r/atom false))
(defonce checking-auth? (r/atom false))

;; ---- api base url example ----
(defonce api-url (r/atom "http://localhost:3000/api"))

;; ---- example of error handler ----
(defn handle-error [response]
  (let [status (:status response)]
    (reset! error-message
            (case status
              401 "Invalid username or password."
              403 "Access denied."
              500 "Server error. Please try again."
              (str "Unexpected error: " status)))))

;; ---- authentication functions ----
(defn check-auth-status []
  (reset! error-message "")
  (reset! checking-auth? true)
  (go
    (let [response (<! (http/get (str @api-url "/auth/status")
                                 {:with-credentials? true}))]
      (reset! checking-auth? false)
      (reset! authenticated? (= 200 (:status response))))))

(defn log-in []
  (reset! loading? true)
  (reset! error-message "")
  (go
    (let [response (<! (http/post (str @api-url "/auth/login")
                                  {:body (js/JSON.stringify #js {:username @username
                                                                  :password @password})
                                   :headers {"Content-Type" "application/json"}
                                   :with-credentials? true}))]
      (reset! loading? false)
      (if (= 200 (:status response))
        (do
          (reset! username "")
          (reset! password "")
          (reset! authenticated? true)
          (js/window.location.reload))
        (handle-error response)))))

(defn register []
  (reset! error-message "")
  (if (not= @password @confirm-password)
    (reset! error-message "Passwords do not match.")
    (do
      (reset! loading? true)
      (let [payload {:username @username
                     :password @password
                     :email @email
                     :birthday @birthday
                     :phone @phone}]
        (go
          (let [response (<! (http/post (str @api-url "/auth/register")
                                        {:body (js/JSON.stringify (clj->js payload))
                                         :headers {"Content-Type" "application/json"}
                                         :with-credentials? true}))]
            (reset! loading? false)
            (if (= 201 (:status response))
              (do
                (reset! username "")
                (reset! password "")
                (reset! confirm-password "")
                (reset! email "")
                (reset! phone "")
                (reset! authenticated? true)
                (js/window.location.reload))
              (handle-error response))))))))

(defn log-out []
  (reset! loading? true)
  (go
    (<! (http/post (str @api-url "/auth/logout")
                   {:with-credentials? true}))
    (reset! loading? false)
    (js/window.location.reload)))

;; function to make authed requests
(defn authed-request
  [method url {:keys [params json-body]}]
  (go
    (let [request-opts (cond-> {:with-credentials? true
                                :headers {"Content-Type" "application/json"}}
                         params (assoc :query-params params)
                         json-body (assoc :body (js/JSON.stringify (clj->js json-body))))
          response (<! (http/request (assoc request-opts :method method :url url)))]
      (if (= 200 (:status response))
        (:body response)
        (do
          (println "Request failed with status" (:status response))
          nil)))))
