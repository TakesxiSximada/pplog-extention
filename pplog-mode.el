;; -*- coding: utf-8 -*-
(require 'request)

(defvar pplog-mode-hook nil)

(defun pplog-post ()
  "POST PPLOG"
  (interactive)
  (request "http://127.0.0.1:8881"
           :type "POST"
           :data (buffer-string)
           :success (lambda (&rest kwds)
                      (print "ok"))))

(defvar pplog-mode-map
  (let ((map (make-keymap)))
    (define-key map "\C-c" 'pplog-post)
    map)
  "Keymap for pplog major mode")

(defun pplog-mode ()
  "pplog-mode"
  (interactive)
  (kill-all-local-variables)
  (setq mode-name "pplog-mode")
  (setq major-mode 'pplog-mode)
  (use-local-map pplog-mode-map)
  (run-hooks 'pplog-mode-hook))

(provide 'pplog-mode)
