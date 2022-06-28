(defun idiotic-concat-many-strings (l)
  ;; concat already accepts multiple arguments...
  (seq-reduce (lambda (acc x)
				(if (zerop (length acc))
					x
				  (concat acc x)))
			  l
			  "")
  )

(setq my-list (list "one" "two" "three"))
(format T "Original list: ~d" my-list)
(terpri)
(format T "Reversed list: ~d" (idiotic-concat-many-strings my-list))
(terpri)
