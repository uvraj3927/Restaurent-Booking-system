# AWS Deployment Checklist

## Pre-Deployment

- [ ] All team members informed of deployment
- [ ] Database backups created
- [ ] Code is committed and pushed to main branch
- [ ] All environment-specific configs prepared
- [ ] AWS credentials configured locally

## Backend Configuration (EC2)

### Code Updates
- [ ] `backend/cors_config.py` created with S3 frontend URL
- [ ] `backend/.env.example` created with RDS connection format
- [ ] `backend/app.py` updated to import and use CORS config
- [ ] All environment variables documented
- [ ] No hardcoded localhost/127.0.0.1 references remain

### Database (RDS)
- [ ] RDS endpoint reachable: `terraform-20260927051125369200000003.cahuiyuc6om9.us-east-1.rds.amazonaws.com:3306`
- [ ] Database `myappdb` exists
- [ ] Database user created with proper permissions
- [ ] Connection string tested: `mysql -h [RDS_ENDPOINT] -u [USER] -p myappdb -e "SELECT 1;"`
- [ ] seeds.py executed to populate initial data

### EC2 Instance Setup
- [ ] SSH access confirmed to 44.200.253.83
- [ ] Python 3 installed: `python3 --version`
- [ ] pip installed: `pip3 --version`
- [ ] MySQL client installed: `mysql --version`
- [ ] Git installed: `git --version`

### Backend Deployment
- [ ] Repository cloned to EC2
- [ ] Virtual environment created: `python3 -m venv venv`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] .env file created with correct database credentials
- [ ] Flask app runs locally: `python app.py`
- [ ] Health endpoint responds: `curl http://44.200.253.83:5000/api/health`
- [ ] Database connection test passes: `curl http://44.200.253.83:5000/api/db-test`

## Frontend Configuration (S3)

### Code Updates
- [ ] `frontend/js/api-config.js` created with API_CONFIG
- [ ] All fetch calls updated to use `apiFetch()` or `apiGet()`, etc.
- [ ] Search for "localhost" in frontend code - none found
- [ ] Search for "127.0.0.1" in frontend code - none found
- [ ] Search for relative "/api/" paths - all converted to full URLs
- [ ] All API URLs point to `http://44.200.253.83:5000`

### S3 Bucket
- [ ] S3 bucket `restaurant-booking-frontend-868ca2b4` exists
- [ ] S3 static website hosting enabled
- [ ] Bucket policy allows public read access
- [ ] index.html is set as index document
- [ ] error.html configured (optional)

### Frontend Deployment
- [ ] Build completed (if using build tool)
- [ ] AWS CLI configured: `aws configure` done
- [ ] AWS credentials have S3 access
- [ ] Files synced to S3: `aws s3 sync ./frontend/ s3://restaurant-booking-frontend-868ca2b4/ --delete`
- [ ] Frontend accessible: http://restaurant-booking-frontend-868ca2b4.s3-website-us-east-1.amazonaws.com
- [ ] Pages load without 404 errors

## Integration Testing

### API Connectivity
- [ ] Frontend loads without console errors
- [ ] Developer console shows no 404 errors
- [ ] No CORS errors in console
- [ ] API calls go to correct endpoint (44.200.253.83:5000)
- [ ] Auth endpoints work (login, register)
- [ ] GET endpoints respond with data
- [ ] POST endpoints accept and process data

### Database Integration
- [ ] User login queries database
- [ ] Restaurant list populates from database
- [ ] Booking creation saves to database
- [ ] Booking retrieval loads from database

### CORS Validation
- [ ] OPTIONS preflight requests succeed
- [ ] Access-Control-Allow-Origin header present
- [ ] Access-Control-Allow-Credentials header present (if needed)
- [ ] No mixed HTTP/HTTPS issues

## Security

- [ ] .env file NOT committed to git
- [ ] Database passwords NOT in code
- [ ] S3 bucket public access reviewed
- [ ] EC2 security group restricts access appropriately
- [ ] RDS security group allows EC2 only
- [ ] HTTPS not yet configured (document for Phase 2)

## Monitoring & Logging

- [ ] Backend logs accessible: `tail -f ~/nohup.out`
- [ ] Error logging configured
- [ ] Database connection pooling set up
- [ ] Application monitoring in place (CloudWatch)

## Documentation

- [ ] AWS_DEPLOYMENT_GUIDE.md completed and committed
- [ ] DEPLOYMENT_CHECKLIST.md (this file) saved
- [ ] Team has access to deployment guide
- [ ] Emergency contacts documented
- [ ] Rollback procedures documented

## Post-Deployment

- [ ] Monitor application for errors (first 24 hours)
- [ ] Check CloudWatch metrics
- [ ] Verify database backups are working
- [ ] Run performance tests
- [ ] Document any issues encountered

## Rollback Plan

If critical issues occur:

1. **Frontend Rollback**
   ```bash
   aws s3 sync ./frontend-backup/ s3://restaurant-booking-frontend-868ca2b4/ --delete
   ```

2. **Backend Rollback**
   ```bash
   cd /home/ec2-user/Restaurent-Booking-system/backend
   git checkout previous-working-commit
   python app.py
   ```

3. **Database Rollback**
   ```bash
   mysql -h [RDS_ENDPOINT] -u [USER] -p myappdb < backup.sql
   ```

---

## Deployment Sign-Off

- **Deployment Date**: ________________
- **Deployed By**: ________________
- **Reviewed By**: ________________
- **Status**: [ ] Success  [ ] Partial  [ ] Rollback
- **Notes**: 
  ```
  
  
  
  ```
