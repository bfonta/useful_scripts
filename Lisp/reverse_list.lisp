(defun rev (l)
  (let (value)
    (dolist (elt l value)
      (setq value (cons elt value))
	  )))

(defparameter my-list (list 1 2 3))
(format T "Original list: ~d" my-list)
(terpri)
(format T "Reversed list: ~d" (rev my-list))
(terpri)
